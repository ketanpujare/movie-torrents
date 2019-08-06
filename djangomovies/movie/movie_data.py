from requests           import session
from lxml.html          import fromstring
from os.path            import exists
from os                 import makedirs
from .models            import Movie
from .utils             import store_movie_data
from cfscrape           import create_scraper
from re                 import sub

class MoviesData:
    def __init__(self,domain,download=False):
        self.domain = domain
        self.download = download

    def download_content(self,link,movie_name,extension,sess,is1080=False):
        
        base_location = 'movie/static/movie'
        def _remove_spaces(name):
            if name:
                return sub('[/ ]+', '_', name)
        
        def _create_directory(pathname):
            if not exists(pathname):
                makedirs(pathname)
        
        if self.download:
            movie_name = _remove_spaces(movie_name)
            if link:
                img = sess.get(link)
            if img.status_code==200:
                _create_directory('{}/{}'.format(base_location, movie_name))
                if not is1080:
                    with open('{}/{}/{}.{}'.format(base_location, movie_name, movie_name,extension),'wb') as f:
                        f.write(img.content)
                else:
                    with open('{}/{}/{}_1080.{}'.format(base_location, movie_name,movie_name,extension),'wb') as f:
                        f.write(img.content)
                return True
            return False
        else:
            print('Download Not Set')


    def get_movie_page(self,link,sess):

        def _check_empty(lst,index):
            try:
                return lst[index]
            except IndexError:
                return None

        def _get_genre(genre):
            nolistgenre = _check_empty(genre,0)
            if nolistgenre:
                return list(i.strip() for i in nolistgenre.split('/'))
            return None

        page = sess.get(link)
        if page.status_code == 200:    
            tree = fromstring(page.content)

            movie_name = tree.xpath('//div[@id="movie-info"]/div[@class="hidden-xs"]/h1[1]/text()')
            movie_year = tree.xpath('//div[@id="movie-info"]/div[@class="hidden-xs"]/h2[1]/text()')
            movie_genre = tree.xpath('//div[@id="movie-info"]/div[@class="hidden-xs"]/h2[2]/text()')
            imdb_link = tree.xpath('//div[@class="bottom-info"]/div/a[@title="IMDb Rating"]/@href')
            down720_link = tree.xpath(
                '//div[@class="bottom-info"]/p[@class="hidden-md hidden-lg"]/a[contains(.,"720p")]/@href')
            down1080_link = tree.xpath(
                '//div[@class="bottom-info"]/p[@class="hidden-md hidden-lg"]/a[contains(.,"1080p")]/@href')
            directors = tree.xpath('//div[@class="directors"]/div/div[2]/a/span/span/text()')
            actors = tree.xpath('//div[@class="actors"]/div/div[2]/a/span/span/text()')
            synopsis = tree.xpath('//div[@id="synopsis"]/p[@class="hidden-xs"]/text()')
            
            movie_image = tree.xpath('//div[@id="movie-poster"]/img/@src')
            bool_image  = self.download_content(_check_empty(movie_image,0),_check_empty(movie_name,0),'jpg',sess)
            bool_720    = self.download_content(_check_empty(down720_link,0),_check_empty(movie_name,0),'torrent',sess)
            bool_1080   = self.download_content(_check_empty(down1080_link,0),_check_empty(movie_name,0),'torrent',sess,True)

            movie_data = {
                'movie_name'    : _check_empty(movie_name,0),
                'movie_year'    : _check_empty(movie_year,0),
                'movie_genre'   : _get_genre(movie_genre),
                'imdb_link'     : _check_empty(imdb_link,0),
                'down720_link'  : _check_empty(down720_link,0) if bool_720 else None,
                'down1080_link' : _check_empty(down1080_link,0) if bool_1080 else None,
                'directors'     : directors,
                'actors'        : actors,
                'synopsis'      : _check_empty(synopsis,0),
                'image'         : bool_image
            }

            store_movie_data(movie_data)

        else:
            print("=================",link)
            with open('miss_movie.txt','a') as f:
                f.write("{}\n".format(link))



    def get_page(self,linkextra):
        sess = session()

        scrape = create_scraper(sess=sess)      # bypass DDoS attack protection

        page = scrape.get('{}{}'.format(self.domain,linkextra))
        tree = fromstring(page.content)

        movie_links = tree.xpath(
            '*//div[@class="browse-movie-wrap col-xs-10 col-sm-4 col-md-5 col-lg-4"]/div/a[1]/@href'
        )
        movie_names = tree.xpath(
            '*//div[@class="browse-movie-wrap col-xs-10 col-sm-4 col-md-5 col-lg-4"]/div/a[1]/text()'
        )

        next_page = tree.xpath(
            '//li[@class="pagination-bordered"]/following-sibling::li/a/@href'
        )

        for movie_name in movie_names:
            if not Movie.objects.filter(movie_name=movie_name): 
                if next_page:
                    print(next_page[0])
                    self.get_page(next_page[0])
                    break

        for movie_name, movie_link in zip(movie_names, movie_links):
            if 'yts' in movie_link:
                print("---------->",movie_name)
                if not Movie.objects.filter(movie_name=movie_name):
                    self.get_movie_page(movie_link, scrape)

        # if next_page:
        #     print(next_page[0])
        #     self.get_page(next_page[0])



def start_data():
    domain = 'https://yts.lt'
    image_download = True
    class_obj = MoviesData(domain,image_download)
    class_obj.get_page('/browse-movies')
