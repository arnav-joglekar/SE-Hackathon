from django.contrib import admin
from django.urls import path,include
from UniVerse import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('todolist/',include('todolist.urls')),
    path('',include('room.urls')),
]
