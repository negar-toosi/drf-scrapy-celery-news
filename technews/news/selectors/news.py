from typing import Optional

from django.db.models import QuerySet
from technews.common.utils import get_object
from technews.news.models import News
from technews.news.filters import NewsFilter
def news_get(news_id) -> Optional[News]:
    news = get_object(News, id=news_id)

    return news

def news_list(*, filters: dict) -> News.objects.all().__class__:
    queryset = News.objects.prefetch_related("tags").filter(status=True)
    news_filter = NewsFilter(filters,queryset=queryset)
    queryset = news_filter.qs
    return queryset.distinct()