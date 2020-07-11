# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import os
import psycopg2


class MockNexusPipeline:
    def process_item(self, item, spider):
        try:
            query = ''
            
            data = item
            
            self.cur.execute(query, data)
            self.connection.commit()
        except:
            self.connection.rollback()
        return item

    def open_spider(self, spider):
        hostname = 'localhost'
        username = os.environ.get('PG_USERNAME')
        password = os.environ.get('PG_PASSWORD')
        database = 'Mock_Nexus'

        self.connection = psycopg2.connect(
            host=hostname,
            user=username,
            password=password,
            dbname=database
        )

    def close_spider(self, spider):
        self.cur.close()
        self.connection.close()

    