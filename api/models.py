from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime

# Create your models here.

class Queries(models.Model):
    time = models.TimeField(default=datetime.datetime.now, auto_now=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='queries')
    query = models.TextField()
    excluding = models.TextField(null=True, blank=True)
    required = models.TextField(null=True, blank=True)
    time = models.TextField(null=True, blank=True)