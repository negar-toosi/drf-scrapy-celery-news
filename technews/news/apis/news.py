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

from drf_spectacular.utils import extend_schema


class NewsDetailApi(APIView):
    class Pagination(LimitOffsetPagination):
        default = 1

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = News
            exclude = ['status', 'created_at', 'summary']
    @extend_schema(responses=OutputSerializer)
    def get(self, request, news_id):
        news = news_get(news_id)

        if news is None:
            raise Http404
        
        data = self.OutputSerializer(news).data

        return Response(data)

class NewsListApi(APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 5

    class FilterSerializer(serializers.Serializer):
        tag = serializers.CharField(max_length=256)

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = News
            fields = ['title', 'summary', 'source', 'tags', 'published_at']
    @extend_schema(request=FilterSerializer, responses=OutputSerializer)
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
            model = News
            exclude = ['updated_at','status']
    @extend_schema(request=InputSerializer)
    def post(self, request):
        serializer = self.InputSerializer(data=request)
        serializer.is_valid(raise_exception=True)

        user = news_create(
            **serializer.validation_data
        )

        data = NewsDetailApi.OutputSerializer(user).data

        return Response(data)