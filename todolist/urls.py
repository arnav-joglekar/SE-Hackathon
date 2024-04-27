from django.urls import path, include
from . import views
from django.contrib import admin

app_name = 'todolist'

urlpatterns = [
    path('', views.index, name='index'),
    path('assignments/', views.assignments, name='assignments'),
]
