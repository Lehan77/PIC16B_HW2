# to run 
# scrapy crawl tmdb_spider -o movies.csv

import os
import scrapy


class TmdbSpider(scrapy.Spider):
    name = 'tmdb_spider'
    
    start_urls = ['https://www.themoviedb.org']

    def parse(self, response):
        # navigate to the Cast & Crew page
        page = response.urljoin("https://www.themoviedb.org/tv/118357-1883/cast")
        # call parse_full_credits method
        yield scrapy.Request(url=page, callback=self.parse_full_credits)

    def parse_full_credits(self, response):
        """
        Assumption: start on the Cast & Crew page.
        Effects: yield a scrapy.Request for the page of each actor listed on the page. Crew members are not included.
                 The yielded request should specify the method parse_actor_page(self, response) should be called when
                 the actor’s page is reached.
        The parse_full_credits() method does not return any data.
        """
        # Redirect to each actor's page and call parse_actor_page method
        # media_v4 > div > div > section:nth-child(1) > ol > li:nth-child(1) > a
        for a in response.css('ol.people')[0].css('li a'):
            if a.xpath('@href').get().startswith('/person'):
                yield scrapy.Request(url=response.urljoin(os.path.join(self.start_urls[0], a.xpath('@href').get())), callback=self.parse_actor_page)

    def parse_actor_page(self, response):
        """
                 Assumption: Start on the page of an actor.
                 Effects: It should yield a dictionary with two key-value pairs, of the form {"actor" : actor_name, "movie_or_TV_name" : movie_or_TV_name}.
                 The method should yield one such dictionary for each of the movies or TV shows on which that actor has worked.
                """
        # Get the actor name
        actor_name = response.xpath('//*[@id="media_v4"]/div/div/div[2]/div/section[1]/div/h2/a/text()').get()
        # get the list of movie or TV name
        movie_or_TV_name = response.xpath('//*[@id="known_for_scroller"]/ul').css('li div a img').xpath('@alt').getall()
        # yield one dictionary for each of the movies or TV shows
        for name in movie_or_TV_name:
            yield {
                'actor': actor_name,
                'movie_or_TV_name': name
            }

        
