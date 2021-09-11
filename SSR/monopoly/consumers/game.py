from channels.generic.websocket import AsyncJsonWebsocketConsumer

from monopoly.consumers.util import games, rooms, decisions, build_add_err_msg, build_init_msg, change_handlers
from monopoly.core.move_receipt import ModalTitleType
from monopoly.game_handlers.game_handler import get_building_type, handle_roll, handle_confirm_decision, \
    handle_cancel_decision, handle_end_game, handle_chat

import logging

logger = logging.getLogger(__name__)


class GameConsumer(AsyncJsonWebsocketConsumer):
    handler_mapping = {
        "roll": handle_roll,
        "confirm_decision": handle_confirm_decision,  # choose yes
        "cancel_decision": handle_cancel_decision,  # choose no
        "end_game": handle_end_game,
        "chat": handle_chat,
    }

    async def receive_json(self, content, **kwargs):
        player = self.scope['user']
        action = content['action']
        logger.info(f'action: {action}')
        if action != 'init':
            msg = await self.handler_mapping[action](h=self.game_id, gs=games, chs=change_handlers, message=content)
        else:
            if (self.game_id not in games) \
                    or (self.game_id not in rooms or player.username not in rooms[self.game_id]):
                msg = await build_add_err_msg()
                return await self.send_json(msg)
            game = games[self.game_id]

            players = game.players
            profiles = rooms[self.game_id]  # get all players in the room

            cash_change = [player.money for player in players]
            pos_change = [player.position for player in players]
            landname = None

            if decisions.get(self.game_id) is not None:  # decision in waiting queue
                wait_decision = "true"
                decision = decisions[self.game_id].beautify()
                landname = decisions[self.game_id].land.description
                next_player_ind = game.cur_player.index

                title_type = ModalTitleType()
                decision_type = decisions[self.game_id].type
                title = title_type.description(decision_type)
            else:  # waiting for decision
                wait_decision = "false"
                decision = None
                next_player_ind = game.cur_player.index
                title = None

            owners = game.get_land_owners()
            houses = []
            for i in range(len(owners)):
                houses.append(get_building_type(i, game))

            msg = await build_init_msg(profiles, cash_change, pos_change, wait_decision, decision, next_player_ind,
                                       title, landname, owners, houses)
            # await self.send_json(msg)
        # Send message to room group
        await self.channel_layer.group_send(
            self.game_id_group,
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
        self.game_id = self.scope['url_route']['kwargs']['game_id']
        self.game_id_group = 'game_%s' % self.game_id
        # Join room group
        await self.channel_layer.group_add(
            self.game_id_group,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.game_id_group,
            self.channel_name
        )
