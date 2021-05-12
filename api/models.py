from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class Queries(models.Model):
    time = models.TimeField(default=timezone.now, auto_now=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='queries')

class Token(models.Model):
    token = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='token')