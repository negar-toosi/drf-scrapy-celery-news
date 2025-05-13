import django_filters
from technews.news.models import News

class NewsFilter(django_filters.FilterSet):
    tag = django_filters.CharFilter(field_name='tags__name', lookup_expr='icontains')
    tags = django_filters.BaseInFilter(field_name='tags__name', lookup_expr='in')
    content = django_filters.CharFilter(field_name='content', lookup_expr='icontains')

    class Meta:
        model = News
        fields = []