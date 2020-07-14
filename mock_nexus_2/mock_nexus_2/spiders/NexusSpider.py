import scrapy
from mock_nexus_2.items import MockNexusItem
from scrapy import Spider, Request
import re
from functools import partial

class NexusSpider(Spider):
    name = 'nexus_spider'
    allowed_domains = ['dailynexus.com']
    start_urls = [

        # News
        'https://dailynexus.com/category/news/campus-news/',
        'https://dailynexus.com/category/news/county/',
        'https://dailynexus.com/category/news/police-blotter-news/',
        'https://dailynexus.com/category/news/feature/',
        'https://dailynexus.com/category/news/isla_vista/',
        'https://dailynexus.com/category/news/student-gov/',
        'https://dailynexus.com/category/news/uc/',
        'https://dailynexus.com/category/news/ucsb-cola-movement/',

        # Sports
        'https://dailynexus.com/category/sports/baseball-sports/',
        'https://dailynexus.com/category/sports/basketball-sports/',
        'https://dailynexus.com/category/sports/columnsfeatures/',
        'https://dailynexus.com/category/sports/cross-country/',
        'https://dailynexus.com/category/sports/golf-sports/',
        'https://dailynexus.com/category/sports/soccer-sports/',
        'https://dailynexus.com/category/sports/softball-sports/',
        'https://dailynexus.com/category/sports/swimming-sports/',
        'https://dailynexus.com/category/sports/tennis-sports/',
        'https://dailynexus.com/category/sports/track-and-field-sports/',
        'https://dailynexus.com/category/sports/volleyball-sports/',
        'https://dailynexus.com/category/sports/water-polo-sports/',
        'https://dailynexus.com/category/sports/track-and-field-sports/',

        # Opinion
        'https://dailynexus.com/category/opinion/argument-in-the-office/',
        'https://dailynexus.com/category/opinion/ask-aj/',
        'https://dailynexus.com/category/opinion/flesh-prison/',
        'https://dailynexus.com/category/opinion/global-gauchos/',
        'https://dailynexus.com/category/opinion/hyphenated-american/',
        'https://dailynexus.com/category/opinion/living/',
        'https://dailynexus.com/category/opinion/letters-to-the-editor/',
        'https://dailynexus.com/category/opinion/politics/',
        'https://dailynexus.com/category/opinion/therapeutic-thoughts/',
        'https://dailynexus.com/category/opinion/virtual-reality/',
        'https://dailynexus.com/category/opinion/wed-hump-opin/',

        # Artsweek
        'https://dailynexus.com/category/artsweek/feature-artsweek/',
        'https://dailynexus.com/category/artsweek/film-and-tv/',
        'https://dailynexus.com/category/artsweek/literature-artsweek/',
        'https://dailynexus.com/category/artsweek/music-artsweek/',
        'https://dailynexus.com/category/artsweek/performing-arts-artsweek/',
        'https://dailynexus.com/category/artsweek/previews-whats-going-on/',
        'https://dailynexus.com/category/artsweek/visual-art-2-artsweek/',

        # Science & Tech
        'https://dailynexus.com/category/science/health-wellness/'

        # Labyrinth - NEEDS SPECIAL TREATMENT
        # 'https://dailynexus.com/category/labyrinth/',

        # On the Menu
        'https://dailynexus.com/category/on-the-menu/coffee-column/',
        'https://dailynexus.com/category/on-the-menu/first-impressions/',
        'https://dailynexus.com/category/on-the-menu/meal-prep-mondays/',
        'https://dailynexus.com/category/on-the-menu/on-the-road/',
        'https://dailynexus.com/category/on-the-menu/recipes-on-the-menu/',
        'https://dailynexus.com/category/on-the-menu/the-beet/',

        # Multimedia
        'https://dailynexus.com/category/multimedia/video/',
        'https://dailynexus.com/category/multimedia/photo/',
        'https://dailynexus.com/category/multimedia/comics/',

        # Nexustentialism
        'https://dailynexus.com/category/nexustentialism/',

        # About - NEEDS SPECIAL TREATMENT
        # 'https://dailynexus.com/advertising/',
        # 'https://dailynexus.com/advertising/classified-ads/',
        # 'https://dailynexus.com/donate/donate-nexus/',
        # 'https://dailynexus.com/faq/',
        # 'https://dailynexus.com/aboutcontact/staff-contact/'

    ]

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
