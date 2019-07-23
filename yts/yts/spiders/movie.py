# -*- coding: utf-8 -*-
from scrapy     import Spider,Request

from pymongo    import MongoClient
import csv

#mongodb connection
client = MongoClient('mongodb://localhost',27017)
db = client['yts-movies']
movies = db.movies

class MovieSpider(Spider):
    name = 'movie'
    url = 'https://yts.lt'

    def remove_comma(self,name):
        return str(name).replace(',','_')

    #csv header
    with open('movies.csv','a') as csvfile:
            datawriter = csv.writer(csvfile,quotechar=',')
            datawriter.writerow(['Movie Name','Movie Year','Movie Genre',
                    'IMDB Link','720p Download Link','1080p Download Link'])

    def start_requests(self):
        yield Request('{}/browse-movies'.format(self.url),
                callback=self.get_hamepage)

    def get_hamepage(self, response):
        movie_page_links = response.xpath(
            '//div[@class="browse-movie-wrap col-xs-10 col-sm-4 col-md-5 col-lg-4"]/a[1]/@href').getall()
        movie_names = response.xpath(
            '//div[@class="browse-movie-wrap col-xs-10 col-sm-4 col-md-5 col-lg-4"]/div/a[1]/text()').getall()
        for movie_name, movie_page in zip(movie_names, movie_page_links):
            
            # if movie not present in database than send request for movie page
            if not movies.find_one({'name':self.remove_comma(str(movie_name.strip()))}):
                yield Request(movie_page,
                        callback=self.get_movie_data)
        
        # check if new downloads appear in front page only ## to avoid unnecessary requests
        next_page = response.xpath('//li[@class="pagination-bordered"]/following-sibling::li/a/@href').get()
        if next_page:
            yield Request('{}{}'.format(self.url,next_page.strip()),
                    callback=self.get_hamepage)
    
    def get_movie_data(self, response):
        movie_name = response.xpath('//div[@id="movie-info"]/div[@class="hidden-xs"]/h1[1]/text()').get()
        movie_year = response.xpath('//div[@id="movie-info"]/div[@class="hidden-xs"]/h2[1]/text()').get()
        movie_genre = response.xpath('//div[@id="movie-info"]/div[@class="hidden-xs"]/h2[2]/text()').get()
        imdb_link = response.xpath('//div[@class="bottom-info"]/div/a[@title="IMDb Rating"]/@href').get()
        download720_link = response.xpath(
            '//div[@class="bottom-info"]/p[@class="hidden-md hidden-lg"]/a[contains(.,"720p")]/@href').get()
        download1080_link = response.xpath(
            '//div[@class="bottom-info"]/p[@class="hidden-md hidden-lg"]/a[contains(.,"1080p")]/@href').get()

        # NOSQL dict
        movie_data = dict()
        movie_data['name'] = self.remove_comma(str(movie_name.strip()))
        movie_data['year'] = movie_year.strip()
        movie_data['genre'] = list(i.strip() for i in movie_genre.split('/'))
        movie_data['imdb_link'] = imdb_link
        movie_data['720p_download_link'] = download720_link
        movie_data['1080p_download_link'] = download1080_link

        # Insert into mongodb database
        movies.insert_one(movie_data)

        # # csv
        # with open('movies.csv','a') as csvfile:
        #     datawriter = csv.writer(csvfile,quotechar=',')
        #     datawriter.writerow([remove_comma(movie_name),remove_comma(movie_year),
        #                         remove_comma(movie_genre),imdb_link,
        #                         download720_link,download1080_link])
