import scrapy
from scrapy import Request, Spider
from mock_nexus_2.items import AuthorItem
from mock_nexus_2.start_urls import start_urls
import re

class AuthorSpider(Spider):
    name = "author_spider"
    allowed_domains = ['dailynexus.com']
    start_urls = start_urls

    def parse(self, response):
        articlePreviews = response.css('.category-page-post')

        for preview in articlePreviews:

            def scrape_article(response):
                item = AuthorItem()
                item['name'] = response.css('.single-post-byline > a::text').get()
                item['biography'] = response.css('.saboxplugin-desc > div > p::text').get()
                item['portrait'] = response.css('.saboxplugin-gravatar > a > img::attr(src)').get()
                return item


            article_page = preview.css('.category-page-post-text > p > a::attr(href)').get()
            if article_page is not None:
                yield response.follow(response.urljoin(article_page), callback=scrape_article)

        set_nav_buttons = response.css('.page-navigation')
        next_page_button_filter_object = filter(lambda btn: btn.css('a::text').get() == 'Next ›', set_nav_buttons)
        next_page = None
        for btn in next_page_button_filter_object:
            next_page = btn.css('a::attr(href)').get()
        if next_page is not None:
            yield Request(response.urljoin(next_page), callback=self.parse)
