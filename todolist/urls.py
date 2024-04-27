from django.urls import path, include
from . import views
from django.contrib import admin

app_name = 'todolist'

urlpatterns = [
    path('', views.index, name='index'),
    path('assignments/', views.assignments, name='assignments'),
    path('selfstudy/', views.selfstudy, name='selfstudy'),
    path('create_assignments/', views.create_assignments, name='create_assignments'),
    path('create_selfstudy/', views.create_selfstudy, name='create_selfstudy'),
    path('complete/<uuid:uuid>', views.complete_selfstudy, name='complete_selfstudy'),
]
