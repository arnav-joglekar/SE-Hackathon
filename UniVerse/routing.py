from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import room.routing  # Importing routing configuration for the 'rooms' app

websocket_urlpatterns = [
    path('ws/', URLRouter(room.routing.websocket_urlpatterns)),
]
