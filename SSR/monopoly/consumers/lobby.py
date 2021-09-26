from channels.generic.websocket import AsyncJsonWebsocketConsumer
from .util import rooms


def build_online_rooms_msg():
    ret = list(map(lambda o: o.__repr__(), rooms.values()))
    return {'lobby': ret}


class LobbyConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def receive_json(self, content, **kwargs):
        action = content['action']
        if action == 'query':
            await self.send_json(build_online_rooms_msg())

    async def disconnect(self, close_code):
        # Called when the socket closes
        await self.close(close_code)
