# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


class MockNexusItem(scrapy.Item):
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
