import scrapy
from mock_nexus_2.items import MockNexusItem
from mock_nexus_2.start_urls import start_urls
from scrapy import Spider, Request
import re
from functools import partial

class NexusSpider(Spider):
    name = 'nexus_spider'
    allowed_domains = ['dailynexus.com']
    start_urls = start_urls

    def parse(self, response):
        category = self.capitalize(''.join(re.findall(r'category/(\w+)/', response.url)[0]))
        subcategory = self.capitalize(response.css('.category-page-cat-name > p::text').get())

        articlePreviews = response.css('.category-page-post')

        for preview in articlePreviews:
            item = MockNexusItem()

            item['category'] = category
            item['subcategory'] = subcategory
            item['full_thumbnail'] = preview.css('.category-page-thumbnail-left > div > a > img::attr(src)').get() or preview.css('.category-page-thumbnail-right > div > a > img::attr(src)').get()
            item['mobile_thumbnail'] = preview.css('.category-page-thumbnail-mobile > div > img::attr(src)').get()
            item['title'] = preview.css('.category-page-post-text > h1 > a::text').get()
            item['publish_date'] = preview.css('.category-post-byline::text').get().split(' by')[0]
            item['author'] = preview.css('.author::text').get()
            item['description'] = preview.css('.category-page-post-text > p::text').get()

            def scrape_article(item, response):
                item['src_url'] = response.url
                item['content'] = response.css('.single-post-content').get()
                return item

            item_bound_scrape_article = partial(scrape_article, item)

            article_page = preview.css('.category-page-post-text > p > a::attr(href)').get()
            if article_page is not None:
                yield response.follow(response.urljoin(article_page), callback=item_bound_scrape_article)

        set_nav_buttons = response.css('.page-navigation')
        next_page_button_filter_object = filter(lambda btn: btn.css('a::text').get() == 'Next ›', set_nav_buttons)
        next_page = None
        for btn in next_page_button_filter_object:
            next_page = btn.css('a::attr(href)').get()
        if next_page is not None:
            yield Request(response.urljoin(next_page), callback=self.parse)
        

    def capitalize(self, string):
        return ''.join([char.upper() if i == 0 else char for i, char in enumerate(list(string))])
