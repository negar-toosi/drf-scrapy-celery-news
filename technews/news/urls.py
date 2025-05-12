from django.urls import path

from technews.news.apis.news import NewsDetailApi
urlpatterns = [
        path('<int:news_id>', NewsDetailApi.as_view() , name='news')
]
