from django.shortcuts import render
from rest_framework.response import Response
from .scraper import newsSearch
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from .models import Queries
from django.contrib.auth import authenticate, login, logout
from rest_framework.schemas import coreapi as coreapi_schema
from rest_framework.schemas import ManualSchema, SchemaGenerator
from rest_framework.compat import coreapi, coreschema
from rest_framework import serializers
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
import datetime

# Create your views here.

class ArticleSerializer(serializers.Serializer):
    source = serializers.CharField()
    title = serializers.CharField()
    articlePreview = serializers.CharField()
    url = serializers.CharField()
    urlToImage = serializers.CharField()
    timePublished = serializers.CharField()

class NewsSerializer(serializers.Serializer):
    status = serializers.CharField()
    error = serializers.CharField(allow_null=True)
    articlesFound = serializers.IntegerField()
    articles = ArticleSerializer(many=True)


# class NewsQuery:
#     def __init__(self, query=None, time=None, exclude=None, require=None):
#         self.query = query
#         self.time = time
#         self.exclude = exclude
#         self.require = require

class News(GenericAPIView):
    """
    get:
        Test
    """
    permission_classes = (IsAuthenticated,)
    serializer_class =  NewsSerializer

    def get_serializer_class(self):
        return self.serializer_class
    
    @extend_schema(
    parameters=[
        OpenApiParameter(
            name="q",
            required=True,
            location=OpenApiParameter.QUERY,
            description="Query string for what you want to search a url for",
        ),
        OpenApiParameter(
            name="exclude",
            required=False,
            location=OpenApiParameter.QUERY,
            description="Space delimited words you don't want included in your results",
        ),
        OpenApiParameter(
            name='time',
            required=False,
            location=OpenApiParameter.QUERY,
            description="A time in the format of x(h/d/m/y) where x is the number of the unit of time and h is hours, d is days, m is months, and y is years"
        ),
        OpenApiParameter(
            name='require',
            required=False,
            location=OpenApiParameter.QUERY,
            description="A string that is required to be in the final result"
        ),
    ],
    examples=[
        OpenApiExample(
            name="cnn",
            response_only=True,
            summary="Query for CNN",
            value={
                    "status": "success",
                    "error": None,
                    "articlesFound": 2,
                    "articles": [
                        {
                            "source": "CNN ",
                            "title": "Steel prices have tripled. Now Bank of America is sounding the alarm",
                            "articlePreview": "New York (CNN Business) A bubble could be brewing in steel stocks. The pandemic brought the American steel industry to its knees last spring, forcing ...",
                            "url": "https://news.google.com/articles/CAIiELnJp7JWtY6Un8ot9uSnVe0qMwgEKioIACIQpzoRSNLEm6QR--MasMLSAioUCAoiEKc6EUjSxJukEfvjGrDC0gIw1KnKBg?hl=en-US&gl=US&ceid=US%3Aen",
                            "urlToImage": "https://lh3.googleusercontent.com/6e7z-gzkOwkEown3GyS8NSLR2H4moZ_MhF3SWz5hJybIrhZbuSnyB0ONZfcAlRWRyIdHI8QUYhpyk4g-7g=-p-df",
                            "timePublished": "2021-05-06T18:40:46Z"
                        },
                        {
                            "source": "CNN ",
                            "title": "Heavy artillery fire on Gaza escalates violence as clashes between Arabs and Jews rock Israeli cities",
                            "articlePreview": "Jerusalem (CNN) Gaza came under heavy artillery fire early Friday morning, amid reports -- later conclusively denied -- that the Israeli army had launched a ...",
                            "url": "https://news.google.com/articles/CAIiEIXgmHlLOtxFaMh1A8VzlPkqMwgEKioIACIQpzoRSNLEm6QR--MasMLSAioUCAoiEKc6EUjSxJukEfvjGrDC0gIw1anKBg?hl=en-US&gl=US&ceid=US%3Aen",
                            "urlToImage": "https://lh3.googleusercontent.com/M1YsVPtoa9dHVnlBRn_NEeg1jblVFapNvpBTZ7g0p3u7SAvDzQAZlfms_f4cCiEyZMq0XSiE6sS4RMHtqKM=-p-df",
                            "timePublished": "2021-05-14T03:42:47Z"
                        }
                    ]
            }
        )
    ]
    )
    def get(self, request):
        # request.user for the user

        response = newsSearch(query=request.GET.get('q', ''), 
            timeRange=request.GET.get('time', ''), 
            excluding=request.GET.get('exclude', ''), 
            requiring=request.GET.get('require', ''))
        
        if response['code'] == 200:
            query = Queries(user=User.objects.get(username=request.user.username), 
                query=request.GET.get('q'), 
                excluding=request.GET.get('exclude', None),
                required=request.GET.get('require', None),
                time=datetime.datetime.now()
            )
            query.save()
        
        return Response(response, status=response['code'])