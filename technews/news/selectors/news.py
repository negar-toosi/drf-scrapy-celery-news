from typing import Optional

from django.db.models import QuerySet
from technews.common.utils import get_object
from technews.news.models import News
from technews.news.filters import NewsFilter
def news_get(news_id) -> Optional[News]:
    news = get_object(News, id=news_id)

    return news

def news_list(*, filters: dict) -> News.objects.all().__class__:
    queryset = News.objects.prefetch_related("tags").all()

    tag = filters.get("tag")
    tags = filters.get("tags")
    content = filters.get("content")

    if tag:
        queryset = queryset.filter(tags__name__icontains=tag)

    if tags:
        queryset = queryset.filter(tags__name__in=tags)

    if content:
        queryset = queryset.filter(content__icontains=content)

    return queryset.distinct()