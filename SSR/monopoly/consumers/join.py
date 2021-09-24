import logging

from channels.generic.websocket import AsyncJsonWebsocketConsumer

from monopoly.consumers.message import build_join_failed_msg, build_join_reply_msg, build_start_msg
from monopoly.consumers.room import Room, RoomStatus
from monopoly.consumers.util import rooms, games, change_handlers, get_user
from monopoly.core.game import Game
from monopoly.handlers.notice_handler import NoticeHandler

logger = logging.getLogger(__name__)


async def add_player(room_name, player_name):
    if room_name not in rooms:
        new_room = Room(room_name)
        new_room.host = player_name
        new_room.join(player_name)
        rooms[room_name] = new_room
    else:
        rooms[room_name].join(player_name)

    if rooms[room_name].status == RoomStatus.FULL:
        return False
    return True


async def handle_start(hostname):
    if hostname not in games:
        room: Room = rooms[hostname]
        player_num = len(room)
        game = Game(player_num)
        games[hostname] = game

        change_handler = NoticeHandler(game, hostname)
        game.add_game_change_listener(change_handler)
        change_handlers[hostname] = change_handler

    return build_start_msg()


class QueryAuthMiddleware:
    """
    Custom middleware (insecure) that takes user IDs from the query string.
    """

    def __init__(self, app):
        # Store the ASGI application we were passed
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope['user'].is_anonymous:
            # Look up user from query string (you should also do things like
            # checking if it is a valid user ID, or if scope["user"] is already
            # populated).
            username = scope["query_string"].decode('utf-8').split("=")[-1]
            scope['user'] = await get_user(username)

        return await self.app(scope, receive, send)


class JoinConsumer(AsyncJsonWebsocketConsumer):

    async def receive_json(self, content, **kwargs):
        player = self.scope['user']
        action = content['action']
        logger.info(f"{player}: {action}")
        if action == 'join':
            if not await add_player(self.room_name, player.username):
                return await self.send_json(build_join_failed_msg())
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
