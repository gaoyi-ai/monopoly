from django.urls import path, include
from rest_framework import routers

from monopoly.api import views

router = routers.DefaultRouter()
router.register(r'register', views.CreateProfileViewSet, basename='api')
router.register(r'login', views.Login, basename='user')
router.register(r'password', views.PasswordViewSet, basename='password')
router.register(r'avatar', views.AvatarViewSet, basename='profile')

urlpatterns = [
    # path('auth/', include('rest_framework.urls')),
    path('', include(router.urls)),
]
