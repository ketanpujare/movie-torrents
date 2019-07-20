# -*- coding: utf-8 -*-
from scrapy import Spider,Request

import csv

class MovieSpider(Spider):
    name = 'movie'
    url = 'https://yts.lt'

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
        for movie_page in movie_page_links:
            yield Request(movie_page,
                    callback=self.get_movie_data)
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

        with open('movies.csv','a') as csvfile:
            datawriter = csv.writer(csvfile,quotechar=',')
            datawriter.writerow([movie_name,movie_year,movie_genre,imdb_link,
                                download720_link,download1080_link])
