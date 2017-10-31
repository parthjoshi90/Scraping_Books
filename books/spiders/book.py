# -*- coding: utf-8 -*-
import scrapy


class BookSpider(scrapy.Spider):
    name = "book"
    allowed_domains = ["toscrape.com"]
    start_urls = ['http://books.toscrape.com']

    def parse(self, response):
        
        for _book in  response.css('article.product_pod'):
            items = {
                "title":_book.css('h3 > a::attr(title)').extract_first(),
                "price":_book.css("div > p::text").extract_first(),
                "status":" ".join(_book.css("div > p::text").extract()[2].split()),
            }
            yield items
            
        next_url = response.css("li.next > a::attr(href)").extract_first()
        if next_url:
            next_url = response.urljoin(next_url)
            yield scrapy.Request(url = next_url, callback=self.parse)