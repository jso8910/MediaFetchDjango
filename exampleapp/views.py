from django.http.response import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from .models import Category
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.authtoken.models import Token
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def delete(request):
    id = request.GET.get('id', None)

    object = Category.objects.filter(id=id, user=User.objects.get(username=request.user.username))

    if not object:
        return JsonResponse({"error": "Id doesn't exist or doesn't belong to you"}, status=400)
    
    object.delete()

    return JsonResponse({"message": "success"}, status=200)

@login_required
def add(request):
    content = request.GET.get('category', None)

    if not content:
        return JsonResponse({"error": "category name missing"}, status=400)
    
    category = Category(category=content, user=User.objects.get(username=request.user.username))
    category.save()
    return JsonResponse({"message": "success", "id": category.id}, status=200)

@login_required
def index(request):
    categories = Category.objects.filter(user=User.objects.get(username=request.user.username))
    return render(request, 'exampleapp/index.html', {
        'categories': categories,
        'token': Token.objects.get(user=User.objects.get(username=request.user.username)).key,
    })

@login_required
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