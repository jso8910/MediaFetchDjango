from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from .models import Category
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.authtoken.models import Token

# Create your views here.

def index(request):
    return render(request, 'exampleapp/layout.html')

def search(request):
    if not request.GET.get('query', None):
        return HttpResponseRedirect(reverse('index'))
    return render(request, 'exampleapp/search.html', {
        'query': request.GET.get('query'),
        'when': request.GET.get('when', None),
        'exclude': request.GET.get('exclude', None),
        'require': request.GET.get('require', None),
        'token': Token.objects.get(user=User.objects.get(username=request.user.username)).key,
    })