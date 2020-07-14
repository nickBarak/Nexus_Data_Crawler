# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import os
import psycopg2
from scrapy.exceptions import DropItem


class MockNexusPipeline:

    def __init__(self):
        self.checked_articles = set()
        self.checked_authors = set()

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
        self.cur = self.connection.cursor()

        print('Connected to PostgreSQL')

    def close_spider(self, spider):
        self.cur.close()
        self.connection.close()

    def process_item(self, item, spider):

        # item is an article
        if (item.get('src_url')):
            if (item['src_url'] in self.checked_articles):
                raise DropItem(f'Dropped duplicate \"{item["title"]}\"')

            else:
                self.checked_articles.add(item['src_url'])
                print('PROCESSING ITEM:', item['title'])
                try:
                    query = 'INSERT INTO articles (src_url, title, author, publish_date, full_thumbnail, mobile_thumbnail, category, subcategory, description, content) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
                    
                    data = (item['src_url'], item['title'], item['author'] or 'Not available', item['publish_date'] or '1 January 1900', item['full_thumbnail'] or 'Not available', item['mobile_thumbnail'] or 'Not available', item['category'], item['subcategory'], item['description'], item['content'])

                    query1 = "UPDATE categories SET articles = array_append(articles, %s) WHERE title = '%s'"

                    data1 = (item['src_url'], item['category'])
                    
                    self.cur.execute(query, data)
                    self.connection.commit()
                    print('SUCCESSFUL INSERTION')
                except:
                    print('FAILED INSERTION')
                    self.connection.rollback()
                return item

        # item is an author
        else:
            if (item['name'] in self.checked_authors):
                raise DropItem(f'Dropped duplicate \"{item["name"]}\"')
            
            else:
                self.checked_authors.add(item['name'])
                try:
                    query = 'INSERT INTO authors (name, biography, portrait) VALUES (%s, %s, %s)'

                    data = (item['name'], item['biography'] or 'Not available', item['portrait'] or 'Not available')

                    self.cur.execute(query, data)
                    self.connection.commit()
                    print('SUCCESSFUL INSERTION')
                except:
                    print('FAILED INSERTION')
                    self.connection.rollback()
                return item
