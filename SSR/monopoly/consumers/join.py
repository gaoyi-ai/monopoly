from channels.generic.websocket import AsyncJsonWebsocketConsumer

from monopoly.consumers.util import rooms, games, change_handlers, get_user, get_profile
from monopoly.core.game import Game
from monopoly.game_handlers.notice_handler import NoticeHandler

import logging

logger = logging.getLogger(__name__)


async def add_player(room_name, player_name):
    if room_name not in rooms:
        rooms[room_name] = set()
        rooms[room_name].add(room_name)
    else:
        rooms[room_name].add(player_name)

    if len(rooms[room_name]) > 4:
        return False
    return True


def build_join_failed_msg():
    ret = {"action": "fail_join"}
    return ret


async def build_join_reply_msg(room_name):
    players = rooms[room_name]
    data = []
    for player in players:
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
        # if rooms.get(self.room_name): rooms.pop(self.room_name)
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
