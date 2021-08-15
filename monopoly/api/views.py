from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from rest_framework import viewsets, status, mixins
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.authtoken.models import Token
from monopoly.api.permissions import IsOwnerOrReadOnly, IsOwner
from monopoly.api.serializers import CreateProfileSerializer, AvatarSerializer, PasswordSerializer
from monopoly.models import Profile


class PasswordViewSet(GenericViewSet, mixins.ListModelMixin, mixins.UpdateModelMixin,
                      mixins.RetrieveModelMixin):
    queryset = User.objects.all()
    serializer_class = PasswordSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsOwner]


class AvatarViewSet(GenericViewSet, mixins.ListModelMixin, mixins.UpdateModelMixin,
                    mixins.RetrieveModelMixin):
    queryset = Profile.objects.all()
    serializer_class = AvatarSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]


class Login(viewsets.ViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = []

    def create(self, request, format=None):
        username = request.data['username']
        password = request.data['password']
        user: User = authenticate(username=username, password=password)
        if user is not None and user.auth_token == request.auth:
            if user.is_active:
                login(request, user)
                ret = {
                    'id': user.id,
                    'username': username,
                    'profile': {
                        'id': user.profile.id,
                    }
                }
                return Response(data=ret, status=status.HTTP_200_OK)
        return Response(data=request.data, status=status.HTTP_404_NOT_FOUND)


class CreateProfileViewSet(GenericViewSet, mixins.CreateModelMixin):
    queryset = Profile.objects.all()
    serializer_class = CreateProfileSerializer
    permission_classes = []
    authentication_classes = []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        headers['Token'] = Token.objects.get(user_id=serializer.data['user']['id'])
        return Response(data=serializer.data, status=status.HTTP_201_CREATED, headers=headers)
