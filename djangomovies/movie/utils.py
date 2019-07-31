from .models        import Movie, Actor, Director, Genre

from .movie_data    import MoviesData


def get_movie_data():
    domain = 'https://yts.lt'
    image_download = True
    class_obj = MoviesData(domain,image_download)
    movies = class_obj.get_page('/browse-movies')

    for one_movie in movies:
        movie_obj, created = Movie.objects.get_or_create(
            movie_name = one_movie['movie_name'],
            movie_year = one_movie['movie_year'],
            defaults ={
                'imdb_link': one_movie['imdb_link'],
                'down720_link': one_movie['down720_link'],
                'down1080_link': one_movie['down1080_link'],
                'image_available': image_download }
        )
        for actor in one_movie['actors']:
            actor_obj, created = Actor.objects.get_or_create(
                actor_name = actor
            )
            actor_obj.movies.add(movie_obj)
            actor_obj.save()

        for director in one_movie['directors']:
            director_obj, created = Director.objects.get_or_create(
                director_name = director,
            )
            director_obj.movies.add(movie_obj)
            director_obj.save()

        for one_genre in one_movie['movie_genre']:
            genre_obj, created = Genre.objects.get_or_create(
                genre = one_genre,
            )
            genre_obj.movies.add(movie_obj)
            genre_obj.save()
