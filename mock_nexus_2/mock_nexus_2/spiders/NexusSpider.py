import scrapy
from mock_nexus_2.items import MockNexusItem
from scrapy import Spider, Request
import re

class NexusSpider(Spider):
    name = 'nexus_spider'
    allowed_domains = ['dailynexus.com']
    start_urls = [

        # News
        'https://dailynexus.com/category/news/campus-news/',
        # 'https://dailynexus.com/category/news/county/',
        # 'https://dailynexus.com/category/news/police-blotter-news/',
        # 'https://dailynexus.com/category/news/feature/',
        # 'https://dailynexus.com/category/news/isla_vista/',
        # 'https://dailynexus.com/category/news/student-gov/',
        # 'https://dailynexus.com/category/news/uc/',
        # 'https://dailynexus.com/category/news/ucsb-cola-movement/',

        # # Sports
        # 'https://dailynexus.com/category/sports/baseball-sports/',
        # 'https://dailynexus.com/category/sports/basketball-sports/',
        # 'https://dailynexus.com/category/sports/columnsfeatures/',
        # 'https://dailynexus.com/category/sports/cross-country/',
        # 'https://dailynexus.com/category/sports/golf-sports/',
        # 'https://dailynexus.com/category/sports/soccer-sports/',
        # 'https://dailynexus.com/category/sports/softball-sports/',
        # 'https://dailynexus.com/category/sports/swimming-sports/',
        # 'https://dailynexus.com/category/sports/tennis-sports/',
        # 'https://dailynexus.com/category/sports/track-and-field-sports/',
        # 'https://dailynexus.com/category/sports/volleyball-sports/',
        # 'https://dailynexus.com/category/sports/water-polo-sports/',
        # 'https://dailynexus.com/category/sports/track-and-field-sports/',

        # # Opinion
        # 'https://dailynexus.com/category/opinion/argument-in-the-office/',
        # 'https://dailynexus.com/category/opinion/ask-aj/',
        # 'https://dailynexus.com/category/opinion/flesh-prison/',
        # 'https://dailynexus.com/category/opinion/global-gauchos/',
        # 'https://dailynexus.com/category/opinion/hyphenated-american/',
        # 'https://dailynexus.com/category/opinion/living/',
        # 'https://dailynexus.com/category/opinion/letters-to-the-editor/',
        # 'https://dailynexus.com/category/opinion/politics/',
        # 'https://dailynexus.com/category/opinion/therapeutic-thoughts/',
        # 'https://dailynexus.com/category/opinion/virtual-reality/',
        # 'https://dailynexus.com/category/opinion/wed-hump-opin/',

        # # Artsweek
        # 'https://dailynexus.com/category/artsweek/feature-artsweek/',
        # 'https://dailynexus.com/category/artsweek/film-and-tv/',
        # 'https://dailynexus.com/category/artsweek/literature-artsweek/',
        # 'https://dailynexus.com/category/artsweek/music-artsweek/',
        # 'https://dailynexus.com/category/artsweek/performing-arts-artsweek/',
        # 'https://dailynexus.com/category/artsweek/previews-whats-going-on/',
        # 'https://dailynexus.com/category/artsweek/visual-art-2-artsweek/',

        # # Science & Tech
        # 'https://dailynexus.com/category/science/health-wellness/'

        # # Labyrinth - NEEDS SPECIAL TREATMENT
        # 'https://dailynexus.com/category/labyrinth/',

        # # On the Menu
        # 'https://dailynexus.com/category/on-the-menu/coffee-column/',
        # 'https://dailynexus.com/category/on-the-menu/first-impressions/',
        # 'https://dailynexus.com/category/on-the-menu/meal-prep-mondays/',
        # 'https://dailynexus.com/category/on-the-menu/on-the-road/',
        # 'https://dailynexus.com/category/on-the-menu/recipes-on-the-menu/',
        # 'https://dailynexus.com/category/on-the-menu/the-beet/',

        # # Multimedia
        # 'https://dailynexus.com/category/multimedia/video/',
        # 'https://dailynexus.com/category/multimedia/photo/',
        # 'https://dailynexus.com/category/multimedia/comics/',

        # # Nexustentialism
        # 'https://dailynexus.com/category/nexustentialism/',

        # # About - NEEDS SPECIAL TREATMENT
        # 'https://dailynexus.com/advertising/',
        # 'https://dailynexus.com/advertising/classified-ads/',
        # 'https://dailynexus.com/donate/donate-nexus/',
        # 'https://dailynexus.com/faq/',
        # 'https://dailynexus.com/aboutcontact/staff-contact/'

    ]

    def parse(self, response):
        articles = []
        category = self.capitalize(''.join(re.findall(r'category/(\w+)/', response.url)[0]))
        subcategory = self.capitalize(response.css('.category-page-cat-name > p::text').get())

        articlePreviews = response.css('.category-page-post')

        for preview in articlePreviews:
            full_thumbnail = preview.css('div[class^="category-page-thumbnail"] > div > a > img::attr(src)').get()
            mobile_thumbnail = preview.css('.mobile > a > img::attr(src)').get()
            title = preview.css('.category-page-post-text > h1 > a::text').get()
            publish_date = preview.css('.category-post-byline::text').get().split(' by')[0]
            author = preview.css('.author::text').get()
            description = preview.css('.category-page-post-text > p::text').get()
            src_url = None
            content = None

            def scrapeArticle(self, response):
                src_url = response.url
                content = response.css('.single-post-content').get()

            article_page = preview.css('.category-page-post-text > p > a::attr(href)').get()
            if article_page is not None:
                response.follow(response.urljoin(article_page), scrapeArticle)

            articles.append(
                MockNexusItem(
                    category,
                    subcategory,
                    full_thumbnail,
                    mobile_thumbnail,
                    title,
                    publish_date,
                    author,
                    description,
                    src_url,
                    content
                )
            )

        next_page = response.css().get()
        if next_page is not None:
            response.follow(response.urljoin(next_page, self.parse))
        
        return articles


    def capitalize(self, string):
        return ''.join([char.upper() if i == 0 else char for i, char in enumerate(list(string))])
