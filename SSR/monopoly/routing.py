from django.urls import re_path

from .consumers.join import JoinConsumer
from .consumers.game import GameConsumer
from .consumers.lobby import LobbyConsumer

websocket_urlpatterns = [
    re_path(r'ws/join/(?P<room_name>\w+)/$', JoinConsumer.as_asgi()),
    re_path(r'ws/game/(?P<game_id>\w+)/$', GameConsumer.as_asgi()),
    re_path(r'ws/lobby/', LobbyConsumer.as_asgi())
]
