from django.urls import path
from accounts import views
from django.conf import settings

app_name='accounts'
urlpatterns = [
    path('',views.index,name="index"),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('signup/', views.signup, name="signup"),
    path('userdetails/', views.userdetails, name="userdetails"),
]