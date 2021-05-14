from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('search', views.search, name='search'),
    path('add', views.add, name='add_category'),
    path('delete', views.delete, name='delete_category'),
]
