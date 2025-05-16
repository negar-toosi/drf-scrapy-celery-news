import json 
import os
import sys
import django


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))
sys.path.append(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.django.base")
django.setup()

from technews.news.models import News

news_path = "scrapy_zoomit/zoomit.json"

with open(news_path, 'r', encoding='utf-8') as f:
    data = json.load(f)
    for news in data:
        News.objects.update_or_create(
            source = news.get("url"),
            defaults={
                "title" : news.get("title"),
                "summary" : news.get("summary"),
                "content" : news.get("content"),
                
                "published_at" : news.get("published_at"),
                "status" : True,
            }   
        )

