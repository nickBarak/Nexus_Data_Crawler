# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field, Item


class MockNexusItem(Item):
    category = Field()
    subcategory = Field()
    full_thumbnail = Field()
    mobile_thumbnail = Field()
    title = Field()
    publish_date = Field()
    author = Field()
    description = Field()
    src_url = Field()
    content = Field()    


class AuthorItem(Item):
    name = Field()
    biography = Field()
    portrait = Field()
