from django.http import Http404
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from technews.api.pagination import( 
    LimitOffsetPagination,
    get_paginated_response
    )
from technews.news.models import News, Tags

from technews.news.selectors.news import news_get, news_list
from technews.news.services.news import news_create

from drf_spectacular.utils import extend_schema, OpenApiParameter

class TagsSerializer(serializers.ModelSerializer):
        class Meta:
            model = Tags
            fields = ("name",)

class NewsDetailApi(APIView):

    class OutputSerializer(serializers.ModelSerializer):
        tags = TagsSerializer(many=True)
        class Meta:
            model = News
            exclude = ['status', 'summary']
    @extend_schema(responses=OutputSerializer)
    def get(self, request, news_id):
        news = news_get(news_id)

        if news is None:
            raise Http404
        
        data = self.OutputSerializer(news).data

        return Response(data)

class NewsListApi(APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 15

    class FilterSerializer(serializers.Serializer):
        tag = serializers.CharField(required=False)
        content = serializers.CharField(required=False)
        exclude_content = serializers.CharField(required=False)
    class OutputSerializer(serializers.ModelSerializer):
        tags = TagsSerializer(many=True)
        class Meta:
            model = News
            fields = ['id','title', 'summary', 'source', 'tags', 'published_at']

    @extend_schema(
        request=None,
        parameters=[
            FilterSerializer,
            OpenApiParameter(name='offset',required=False, type=int),],
        responses=OutputSerializer(many=True),
    )
    def get(self, request):
        filters_serializer = self.FilterSerializer(data=request.query_params)
        filters_serializer.is_valid(raise_exception=True)

        news = news_list(filters=filters_serializer.validated_data)

        return get_paginated_response(
            pagination_class=self.Pagination,
            serializer_class=self.OutputSerializer,
            queryset=news,
            request=request,
            view=self
        )

class NewsCreateApi(APIView):

    class InputSerializer(serializers.Serializer):
        title = serializers.CharField(max_length=256)
        content = serializers.CharField()
        summary = serializers.CharField()
        source = serializers.URLField()
        tags = serializers.ListField(
            child=serializers.CharField(max_length=100), allow_empty=True
        )
        published_at = serializers.DateTimeField()
    @extend_schema(request=InputSerializer)
    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        news = news_create(
            **serializer.validated_data
        )

        data = NewsDetailApi.OutputSerializer(news).data

        return Response(data)