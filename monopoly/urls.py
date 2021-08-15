from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.urls import path

from project.settings.base import MEDIA_ROOT, MEDIA_URL
from .views import *

urlpatterns = [
    path('join/', login_required(JoinView.as_view()), name="join"),
    path('join/<str:host_name>/', login_required(JoinView.as_view()), name="join"),
    path('game/<str:host_name>/', login_required(GameView.as_view()), name='game'),

    path('', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/<str:username>/', login_required(ProfileView.as_view()), name='profile'),
    path('logout/', auth_views.logout_then_login, name='logout'),
] + static(MEDIA_URL, document_root=MEDIA_ROOT)
