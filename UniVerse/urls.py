from django.contrib import admin
from django.urls import path,include
from UniVerse import views
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('',views.home,name="home"),
    path('admin/', admin.site.urls),
 
    path('accounts/', include('accounts.urls')),
    path('notes/', include('notes.urls')),

    path('resources/', include('resources.urls')),

    path('rooms/', include('room.urls')),
    path('connect/', include('connections.urls')),
    path('todolist/',include('todolist.urls')),
    path('dashboard/',views.dashboard,name="dashboard")
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)