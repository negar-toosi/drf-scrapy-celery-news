from django.test import TestCase

from technews.news.models import News
from technews.news.selectors.news import news_list
from technews.news.tests.factories import NewsFactory, TagsFactory

class TestNewsList(TestCase):

    def test_filters_by_tags(self):
        tag1 = TagsFactory.create(name='tech')
        news1 = NewsFactory.create(tags=[tag1], status=True)
        
        tag2 = TagsFactory.create(name='Iran')
        news2 = NewsFactory.create(tags=[tag2],status=True)

        result = news_list(filters={"tag":"Tech"})
        
        self.assertIn(news1, result)
        self.assertNotIn(news2, result)

    def test_filters_by_content(self):
        news1 = NewsFactory.create(content='python',status=True)
        news2 = NewsFactory.create(content='java',status=True)

        result = news_list(filters={"content":"python"})

        self.assertIn(news1, result)
        self.assertNotIn(news2, result)

    def test_filters_by_exclude_content(self):
        news1 = NewsFactory.create(content='react',status=True)
        news2 = NewsFactory.create(content='python',status=True)

        result = news_list(filters={'exclude_content':'python'})

        self.assertIn(news1, result)
        self.assertNotIn(news2, result)

    def test_filters_by_content_and_exclude_content(self):
        news = NewsFactory.create(content='python is a programming language',status=True)

        result1 = news_list(filter={'content':'python','exclude_content':'programming'})
        result2 = news_list(filter={'content':'python','exclude_content':'Released'})

        self.assertNotIn(news, result1)
        self.assertIn(news, result2)
