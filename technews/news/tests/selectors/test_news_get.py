
from django.test import TestCase

from technews.news.selectors.news import news_get
from technews.news.tests.factories import NewsFactory

class TestNewsGet(TestCase):
    def test_returns_news_when_exists(self):
        news = NewsFactory.create()
        result = news_get(news.id)
        self.assertEqual(result, news)

    def test_returns_none_when_news_does_not_exist(self):
        news = NewsFactory.create()
        id = news.id
        news.delete()

        result = news_get(id)

        self.assertIsNone(result)

    
        