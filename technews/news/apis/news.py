from django.http import Http404
from rest_framework import status, serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from technews.api.pagination import( 
    LimitOffsetPagination,
    get_paginated_response
    )
from technews.news.models import News

from technews.news.selectors.news import news_get, news_list
from technews.news.services.news import news_create

class NewsDetailApi(APIView):
    class Pagination(LimitOffsetPagination):
        default = 1

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            models = News
            exclude = ['status', 'created_at', 'summery']

    def get(self, request, news_id):
        news = news_get(news_id)

        if news is None:
            raise Http404
        
        data = self.OutputSerializer(user).data

        return Response(data)

class NewsListApi(APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 5

    class FilterSerializer(serializers.Serializer):
        tag = serializers.CharField(max_length=256)

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            models = News
            fields = ['title', 'summary', 'source', 'tags', 'published_at']

    def get(self, request):
        filters_serializer = self.FilterSerializer(data=request.query_params)
        filters_serializer.is_valid(raise_exception=True)

        news = news_list(filters=filters_serializer.validation_data)

        return get_paginated_response(
            pagination_class = self.Pagination,
            serializer_class = self.OutputSerializer,
            queryset = news,
            request = request,
            view = self
        )
    

class NewsCreateApi(APIView):
    class InputSerializer(serializers.ModelSerializer):
        class Meta:
            models = News
            exclude = ['updated_at','status']

    def post(self, request):
        serializer = self.InputSerializer(data=request)
        serializer.is_valid(raise_exception=True)

        user = news_create(
            **serializer.validation_data
        )

        data = NewsDetailApi.OutputSerializer(user).data

        return Response(data)