# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import os
import django
from itemadapter import ItemAdapter

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.django.base')
django.setup()

from technews.news.tasks import save_zoomit_data

class ScrapyZoomitPipeline:

    def __init__(self):
        self.news = []
    def process_item(self, item, spider):
        news_data = ItemAdapter(item).asdict()
        self.news.append(news_data)
        return item
    def close_spider(self, spider):
        if self.news:
            save_zoomit_data.delay(news=self.news)
