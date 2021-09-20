from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from .models import Profile


class GameView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'game_view.html', {
            "username": request.user.username,
            "hostname": kwargs.get("host_name")
        })


class JoinView(View):

    def get(self, request, *args, **kwargs):
        user = request.user
        host_name = kwargs.get('host_name', user.username)
        avatar = Profile.objects.get(user=user).avatar
        # Determine if a custom avatar has been uploaded
        avatar = avatar.url if avatar.name else ''

        return render(request, 'join_view.html', {
            "user": {
                "name": user.username,
                "avatar": avatar
            },
            "host_name": host_name if len(host_name) else user.username
        })


class LoginView(View):
    initial = {'active_page': 'register'}
    template_name = 'login_view.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {
            "active_page": "login",
            "error": None
        })

    def post(self, request, *args, **kwargs):
        next_redirect = request.GET.get('next', reverse('join'))
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect(next_redirect)
            else:
                res = {'active_page': 'login',
                       "error": "Inactive user."}
                return render(request, self.template_name, res)
        else:
            res = {'active_page': 'login',
                   "error": "Invalid username or password."}
            return render(request, self.template_name, res)


class RegisterView(View):
    initial = {'active_page': 'register'}
    template_name = 'login_view.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.initial)

    def _register(self, conf):

        error_message = "Error: "
        for (key, value) in conf.items():
            if not value or len(value) == 0:
                error_message += key + " can't be empty."
                return False, error_message

        if len(User.objects.filter(username=conf["username"])):
            error_message += "the username isn't available. Please try another."
            return False, error_message

        user = User.objects.create_user(
            username=conf["username"],
            password=conf["password"],
        )
        Profile.objects.create(user=user)

        return True, user

    def post(self, request, *args, **kwargs):
        conf = {
            "username": request.POST.get("username", None),
            "password": request.POST.get("password", None),
        }

        successful, auth_or_error = self._register(conf)

        if successful:
            login(request, auth_or_error)
            return redirect(reverse('join'))
        else:
            res = {'active_page': 'register',
                   "error": auth_or_error}
            return render(request, self.template_name, res)


class ProfileView(View):
    template_name = 'profile_view.html'

    def get(self, request, *args, **kwargs):
        user = request.user
        avatar = Profile.objects.get(user=user).avatar
        avatar = avatar if avatar.name else ''
        res = {
            "user": user,
            "avatar": avatar
        }
        return render(request, self.template_name, res)

    def post(self, request, *args, **kwargs):
        self.user = User.objects.get(username=kwargs.get("username"))

        if self.user != request.user:
            raise PermissionDenied

        avatar = request.FILES.get("avatar", None)
        self.profile = Profile.objects.get(user=self.user)
        if avatar:
            self.profile.avatar = avatar
            self.profile.save()

        res = {
            "user": self.user,
            "avatar": self.profile.avatar
        }
        return render(request, self.template_name, res)
