from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from rest_framework.authtoken.models import Token
import random
from api.models import Queries
import datetime
import pygal

# Create your views here.

def logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def index(request):
    if request.user.is_authenticated:
        token = Token.objects.get(user=User.objects.get(username=request.user.username))
        print(token.key)
    return render(request, 'mainsite/index.html') 

# NOT A VIEW
def timeList(time):
    list = time.split('-')
    for i in range(len(list)):
        list[i] = int(list[i])
    return list


def allUsersSvg(request):
    queries = Queries.objects.filter()

    startStr = queries[0].time.split(' ')[0]
    endStr = queries.reverse()[0].time.split(' ')[0]

    start = timeList(startStr)
    end = timeList(endStr)

    line_chart = pygal.Line(fill=True, \
                            interpolate='cubic', \
                            style=pygal.style.DarkSolarizedStyle)
    line_chart.title = "Number of API calls per day (only you)"
    starting = datetime.date(start[0], start[1], start[2])
    ending = datetime.date(end[0], end[1], end[2])
    delta = datetime.timedelta(days=1)
    labels = []
    labels.append(str(starting - delta))
    while starting <= ending:
        labels.append(str(starting))
        starting += delta

    line_chart.x_labels = labels

    calls_per_day = {label:0 for label in labels}
    for i in range(len(labels)):
        for j in range(len(queries)):
            if queries[j].time.split(' ')[0] == labels[i]:
                calls_per_day[labels[i]] += 1
    line_chart.add('API Calls', [i for i in calls_per_day.values()])

    return HttpResponse(line_chart.render(disable_xml_declaration=True, fill=True), content_type="image/svg+xml")

@login_required
def yourUserSvg(request):
    queries = Queries.objects.filter(user=User.objects.get(username=request.user.username))

    startStr = queries[0].time.split(' ')[0]
    endStr = queries.reverse()[0].time.split(' ')[0]

    start = timeList(startStr)
    end = timeList(endStr)

    line_chart = pygal.Line(fill=True, \
                            interpolate='cubic', \
                            style=pygal.style.DarkSolarizedStyle)
    line_chart.title = "Number of API calls per day (all users)"
    starting = datetime.date(start[0], start[1], start[2])
    ending = datetime.date(end[0], end[1], end[2])
    delta = datetime.timedelta(days=1)
    labels = []
    labels.append(str(starting - delta))
    while starting <= ending:
        labels.append(str(starting))
        starting += delta

    line_chart.x_labels = labels

    calls_per_day = {label:0 for label in labels}
    for i in range(len(labels)):
        for j in range(len(queries)):
            if queries[j].time.split(' ')[0] == labels[i]:
                calls_per_day[labels[i]] += 1
    line_chart.add('API Calls', [i for i in calls_per_day.values()])

    return HttpResponse(line_chart.render(disable_xml_declaration=True, fill=True), content_type="image/svg+xml")

@login_required
def dashboard(request):
    exampleQueries = ['coronavirus',
                    'cnn',
                    'fox news',
                    'zoo',
                    'iphone',
                    'android',
                    'forbes',
                    'entertainment',
                    'england',
                    'technology',
                    'bbc',
                    'google',
                    'amazon',
                    'wall street',
                    'latin america',
                    'australia',
                    'science',
                    'physics',
                    'chemistry',
                    'dow jones']
    

    
    return render(request, "mainsite/dashboard.html", {
        "token": Token.objects.get(user=User.objects.get(username=request.user.username)).key,
        "query": random.choice(exampleQueries),
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