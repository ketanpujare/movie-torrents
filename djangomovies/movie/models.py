from django.db  import models
from re         import sub

# Create your models here.

class Movie(models.Model):
    movie_name = models.CharField(max_length=250, unique=True, blank=False, null=False)
    movie_year = models.IntegerField()
    imdb_rating = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    imdb_link = models.URLField(blank=True, null=True)
    down720_link = models.URLField(blank=True, null=True)
    down1080_link = models.URLField(blank=True, null=True)
    image_available = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} {}'.format(self.movie_name, self.movie_year)

    def human_readable_name(self):
        return sub('[/ ]+', '_', self.movie_name)

class Actor(models.Model):
    actor_name = models.CharField(max_length=100, blank=False, null=False)
    movies = models.ManyToManyField(Movie)

    def __str__(self):
        return self.actor_name

class Director(models.Model):
    director_name = models.CharField(max_length=100, blank=False, null=False)
    movies = models.ManyToManyField(Movie)
    
    def __str__(self):
        return self.director_name

class Genre(models.Model):
    genre = models.CharField(max_length=100, blank=False, null=False)
    movies = models.ManyToManyField(Movie)

    def __str__(self):
        return self.genre