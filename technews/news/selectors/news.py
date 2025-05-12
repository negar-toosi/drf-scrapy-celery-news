from typing import Optional

from django.db.models import QuerySet
from technews.common.utils import get_object
from technews.news.models import News

def news_get(news_id) -> Optional[News]:
    news = get_object(News, id=news_id)

    return news

def news_list():
    pass