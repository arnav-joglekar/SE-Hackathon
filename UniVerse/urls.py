from django.contrib import admin
from django.urls import path,include
from UniVerse import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('rooms/', include('room.urls')),
    path('',views.home,name="home")
]
