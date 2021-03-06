from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.urls import path

from .views import *

urlpatterns = [
    path('', login_required(JoinView.as_view()), name="join"),
    path('join/<str:host_name>/', login_required(JoinView.as_view()), name="join"),
    path('game/<str:host_name>/', login_required(GameView.as_view()), name='game'),

    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/<str:username>/', login_required(ProfileView.as_view()), name='profile'),
    path('logout/', auth_views.logout_then_login, name='logout'),
]
