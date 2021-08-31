from channels.generic.websocket import AsyncJsonWebsocketConsumer

from monopoly.consumers.util import rooms, games, change_handlers, get_user, get_profile
from monopoly.core.game import Game
from monopoly.game_handlers.notice_handler import NoticeHandler

# "{'type': 'websocket', 'path': '/ws/join/gaoyi/', 'raw_path': b'/ws/join/gaoyi/', 'headers': [(b'host', " \
# "b'127.0.0.1:8000'), (b'user-agent', b'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 " \
# "Firefox/90.0'), (b'accept', b'*/*'), (b'accept-language', b'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5," \
# "en-US;q=0.3,en;q=0.2'), (b'accept-encoding', b'gzip, deflate'), (b'sec-websocket-version', b'13'), " \
# "(b'origin', b'http://127.0.0.1:8000'), (b'sec-websocket-extensions', b'permessage-deflate'), " \
# "(b'sec-websocket-key', b'9yWLU2epLrYro5zc5LduKQ=='), (b'connection', b'keep-alive, Upgrade'), (b'cookie', " \
# "b'csrftoken=ditypApnmVtP06QGzIYNExt87FNr1O5UxWjK8qb5pXAYGHqNwJYnQvFjKALL77Bd; " \
# "sessionid=7hz4ojsyrf77c2g8g85ak04y3u8d5bd8'), (b'sec-fetch-dest', b'websocket'), (b'sec-fetch-mode', " \
# "b'websocket'), (b'sec-fetch-site', b'same-origin'), (b'pragma', b'no-cache'), (b'cache-control', " \
# "b'no-cache'), (b'upgrade', b'websocket')], 'query_string': b'', 'client': ['127.0.0.1', 55001], 'server': [" \
# "'127.0.0.1', 8000], 'subprotocols': [], 'asgi': {'version': '3.0'}, 'cookies': {'csrftoken': " \
# "'ditypApnmVtP06QGzIYNExt87FNr1O5UxWjK8qb5pXAYGHqNwJYnQvFjKALL77Bd', 'sessionid': " \
# "'7hz4ojsyrf77c2g8g85ak04y3u8d5bd8'}, 'session': <django.utils.functional.LazyObject object at " \
# "0x000002D74A939280>, 'user': <channels.auth.UserLazyObject object at 0x000002D74A9392B0>, 'path_remaining': " \
# "'', 'url_route': {'args': (), 'kwargs': {'room_name': 'gaoyi'}}} "
import logging

logger = logging.getLogger(__name__)


async def add_player(room_name, player_name):
    if room_name not in rooms:
        rooms[room_name] = set()
        rooms[room_name].add(room_name)

    if len(rooms[room_name]) >= 4:
        return False

    rooms[room_name].add(player_name)
    return True


def build_join_failed_msg():
    ret = {"action": "fail_join"}
    return ret


async def build_join_reply_msg(room_name):
    players = rooms[room_name]
    logger.info('players: ', players)
    data = []
    for player in players:
        logger.info('cur :', player)
        user = await get_user(player)
        profile = await get_profile(user)
        avatar = profile.avatar.url if profile.avatar.name else ''
        data.append({"name": player, "avatar": avatar})

    ret = {"action": "join", "data": data}
    return ret


def build_start_msg():
    ret = {"action": "start"}
    return ret


async def handle_start(hostname):
    if hostname not in games:
        players = rooms[hostname]
        player_num = len(players)
        game = Game(player_num)
        games[hostname] = game

        change_handler = NoticeHandler(game, hostname)
        game.add_game_change_listener(change_handler)
        change_handlers[hostname] = change_handler

    return build_start_msg()


class JoinConsumer(AsyncJsonWebsocketConsumer):

    async def receive_json(self, content, **kwargs):
        player = self.scope['user']
        logger.info(f"player: {player.username}")
        action = content['action']
        logger.info(f"{player}: {action}")
        if action == 'join':
            if not await add_player(self.room_name, player.username):
                msg = build_join_failed_msg()
            else:
                msg = await build_join_reply_msg(self.room_name)
        else:  # action == 'start':
            msg = await handle_start(self.room_name)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'game_message',
                'msg': msg
            }
        )

    # Receive message from room group
    async def game_message(self, event):
        msg = event['msg']

        # Send message to WebSocket
        await self.send_json(msg)

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'monopoly_%s' % self.room_name
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
