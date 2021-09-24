from channels.generic.websocket import AsyncJsonWebsocketConsumer

from monopoly.consumers.room import Room, RoomStatus
from monopoly.consumers.util import games, rooms, decisions, change_handlers
from monopoly.consumers.message import build_init_msg, build_add_err_msg, build_ready_msg
from monopoly.core.move_receipt import ModalTitleType
from monopoly.handlers.game_handler import get_building_type, handle_roll, handle_confirm_decision, \
    handle_cancel_decision, handle_end_game, handle_chat, handle_ready
from monopoly.core.game import GameStateType
import logging

logger = logging.getLogger(__name__)


class GameConsumer(AsyncJsonWebsocketConsumer):
    handler_mapping = {
        "roll": handle_roll,
        "confirm_decision": handle_confirm_decision,  # choose yes
        "cancel_decision": handle_cancel_decision,  # choose no
        "end_game": handle_end_game,
        "chat": handle_chat,
        "ready": handle_ready
    }

    async def receive_json(self, content, **kwargs):
        player = self.scope['user']
        action = content['action']
        logger.info(f'{player}: game - {action}')
        if action == 'ready':
            msg = build_ready_msg(handle_ready(h=self.game_id, player=player))
        elif action != 'init':
            msg = await self.handler_mapping[action](h=self.game_id, gs=games, chs=change_handlers, message=content)
        else:
            if (self.game_id not in games) \
                    or (self.game_id not in rooms or player.username not in rooms[self.game_id].players):
                return await self.send_json(build_add_err_msg())
            game = games[self.game_id]
            if game.game_state != GameStateType.INITED:
                return
            game.game_state = GameStateType.WAIT_FOR_ROLL

            players = game.players
            room: Room = rooms[self.game_id]
            room.status = RoomStatus.GAMING
            players_name = room.players  # get all players in the room
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

            msg = await build_init_msg(players_name, cash_change, pos_change, wait_decision, decision, next_player_ind,
                                       title, landname, owners, houses)

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
