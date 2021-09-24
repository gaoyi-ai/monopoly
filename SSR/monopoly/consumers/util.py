from channels.db import database_sync_to_async
from django.contrib.auth.models import User, AnonymousUser

from monopoly.models import Profile

rooms = {}
games = {}
change_handlers = {}
decisions = {}
readys = {}


@database_sync_to_async
def get_user(player):
    try:
        return User.objects.get(username=player)
    except User.DoesNotExist:
        return AnonymousUser()


@database_sync_to_async
def get_profile(user):
    return Profile.objects.get(user=user)
