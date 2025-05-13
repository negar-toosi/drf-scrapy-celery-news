from datetime import datetime
from django.utils import timezone

from django.db import transaction
from technews.news.models import News, Tags

@transaction.atomic
def news_create( 
    *, title: str, summary:str, content: str, source: str, tags: list[str], published_at: datetime,
    ) -> News:

    tags_objects = [Tags.objects.get_or_create(name=name)[0] for name in tags]
    
    news = News.objects.create(
        title = title,
        summary = summary,
        content = content,
        source = source,
        published_at = published_at,
        status = True
    )
    news.tags.set(tags_objects)

    return news


