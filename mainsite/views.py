from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError

# Create your views here.

def logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def index(request):
    return render(request, 'mainsite/index.html') 


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
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
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, 'mainsite/login.html')