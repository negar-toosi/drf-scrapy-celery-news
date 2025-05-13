from django.urls import path

from technews.news.apis.news import NewsDetailApi, NewsCreateApi, NewsListApi
urlpatterns = [
        path('', NewsListApi.as_view() , name='list'),
        path('<int:news_id>/', NewsDetailApi.as_view() , name='news'),
        path('create/', NewsCreateApi.as_view() , name='create')
]
