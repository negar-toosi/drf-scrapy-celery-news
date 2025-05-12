from django.urls import path, include

urlpatterns = [
        path('news/', include(('technews.news.urls', 'news')))
]
