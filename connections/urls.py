from django.urls import path
from connections import views
from django.conf import settings

app_name='connections'
urlpatterns = [
    path('',views.connect,name="connect"),
    path('send_friend_request/<int:receiver_id>/', views.send_friend_request, name='send_friend_request'),
    path('friends/', views.friends, name='friends'),
    path('send_message/', views.send_message, name='send_message'),
]