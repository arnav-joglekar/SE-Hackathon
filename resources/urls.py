from django.urls import path
from resources import views
from django.conf import settings

app_name='resources'
urlpatterns = [
    path('',views.index,name="index"),
   
]