from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from rest_framework.authtoken.models import Token

# Create your views here.

def logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def index(request):
    if request.user.is_authenticated:
        token = Token.objects.get(user=User.objects.get(username=request.user.username))
        print(token.key)
    return render(request, 'mainsite/index.html') 

@login_required
def dashboard(request):
    return render(request, "mainsite/dashboard.html", {
        "token": Token.objects.get(user=User.objects.get(username=request.user.username)).key
    })

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, 'mainsite/login.html', {
                "message": "Invalid username and/or password"
            })
    else:
        return render(request, 'mainsite/login.html')

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')

        password = request.POST.get('password')
        confirm = request.POST.get('confirmation')
        if password != confirm:
            return render(request, 'mainsite/register.html', {
                "message": "Passwords must match"
            })
        
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        Token.objects.get_or_create(user=user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, 'mainsite/register.html')