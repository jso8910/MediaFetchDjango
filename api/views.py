from django.shortcuts import render
from rest_framework.response import Response
from .scraper import newsSearch
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

# Create your views here.

class News(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        # request.user for the user
        return Response(newsSearch(query=request.GET.get('q', ''), 
            timeRange=request.GET.get('time', ''), 
            excluding=request.GET.get('exclude', ''), 
            requiring=request.GET.get('require', '')))