from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from scrapy_zoomit.spiders.zoomit import ZoomitSpider 

from technews.news.services.news import news_create

from celery import shared_task
from asgiref.sync import sync_to_async
@shared_task
def run_spider():
    process = CrawlerProcess(get_project_settings())
    process.crawl(ZoomitSpider)
    process.start(stop_after_crawl=False)
    print(process)

@shared_task
def save_zoomit_data(*, news):
    for n in news:
        news_create(
            title = n.get("title"),
            summary = n.get("summary"),
            content = n.get("content"),
            source = n.get("url"),
            tags = [],
            published_at = n.get("published_at"),
        )
