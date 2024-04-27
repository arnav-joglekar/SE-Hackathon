from django.contrib import admin
from django.urls import path,include
from UniVerse import views
from todolist import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    # path('',views.home,name='home')
    path('todolist/',include('todolist.urls'))
]
