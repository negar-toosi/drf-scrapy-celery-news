from django.utils import timezone
from django.test import TestCase
from technews.news.services.news import news_create
from technews.news.models import News
from technews.utils.test.base import faker



class TestNewsCreate(TestCase):

    def test_creates_news_with_tags(self):
        
        title = faker.sentence()
        summary = faker.paragraph()
        content = faker.text()
        source = faker.url()
        published_at = timezone.make_aware(faker.date_time_between_dates(datetime_start='now'))
        tags = ["django", "python"]

        
        news = news_create(
            title=title,
            summary=summary,
            content=content,
            source=source,
            tags=tags,
            published_at=published_at,
        )

        
        self.assertIsInstance(news, News)
        self.assertEqual(news.title, title)
        self.assertEqual(news.summary, summary)
        self.assertEqual(news.content, content)
        self.assertEqual(news.source, source)
        self.assertEqual(news.status, True)
        self.assertEqual(news.tags.count(), 2)

        tag_names = list(news.tags.values_list("name", flat=True))
        for tag in tags:
            self.assertIn(tag, tag_names)
