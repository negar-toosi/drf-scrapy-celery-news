import django_filters
from technews.news.models import News

class NewsFilter(django_filters.FilterSet):
    tag = django_filters.CharFilter(field_name='tags__name', lookup_expr='icontains')
    content = django_filters.CharFilter(field_name='content', lookup_expr='icontains')
    exclude_content = django_filters.CharFilter(method='filter_exclude_content')

    class Meta:
        model = News
        fields = []

    def filter_exclude_content(self, queryset, name, value):
        return queryset.exclude(content__icontains=value)