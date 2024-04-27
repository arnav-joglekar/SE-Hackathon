from django.contrib import admin
from django.urls import path,include
from UniVerse import views

urlpatterns = [
    path('',views.home,name="home"),
    path('admin/', admin.site.urls),

    path('accounts/', include('accounts.urls')),

    path('resources/', include('resources.urls')),

    path('rooms/', include('room.urls')),
    path('connect/', include('connections.urls')),
    path('',views.home,name='home'),
    path('todolist/',include('todolist.urls'))
]
