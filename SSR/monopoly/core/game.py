from typing import Union, Optional

from monopoly.core.card_deck import CardDeck
from monopoly.core.dice import Dice
from monopoly.core.land import LandType, Land, Constructable, Infrastructure, START_REWARD
from monopoly.core.board import Board
from monopoly.core.move_receipt import MoveReceipt, MoveReceiptType
from monopoly.core.player import Player
from monopoly.core.util import DebugLogHandler

import logging

logger = logging.getLogger(__name__)


class GameStateType:
    WAIT_FOR_ROLL = 0
    WAIT_FOR_DECISION = 1
    GAME_ENDED = 2
    INITED = 3


class Game:
    game_id = 0

    def __init__(self, player_num):
        # assert 0 < player_num <= 4
        if player_num <= 0 or player_num > 4:
            self.notify_error("Error: Incorrect player number, should be 1-4 players.")
            return
        self.players = [Player(i) for i in range(player_num)]
        self.game_state = GameStateType.INITED
        self._card_deck = CardDeck()
        self._board = Board()
        self._dice = Dice()
        self._current_player_index = 0
        self._move_receipt = None
        self._handlers = []
        self.add_game_change_listener(DebugLogHandler(self))
        self._update_game_id()
        self.notify_new_game()

    def _update_game_id(self):
        self.game_id = Game.game_id
        Game.game_id += 1

    @property
    def cur_player(self):
        return self.players[self._current_player_index]

    def player_index_of(self, i) -> Optional[Player]:
        if len(self.players) > i >= 0:
            return self.players[i]
        return None

    def _change_player(self):
        self._current_player_index = self._change_player_on(self._current_player_index)
        self.notify_player_changed()

    def _change_player_on(self, cur):
        new_user_index = (cur + 1) % (len(self.players))
        logger.info(f"new_user_index: {new_user_index}")
        new_user = self.players[new_user_index]
        if new_user.remaining_stop > 0:  # the next player is in stopping
            new_user.deduct_stop(1)
            return self._change_player_on(new_user_index)
        else:
            return new_user_index

    def add_game_change_listener(self, handler):
        self._handlers.append(handler)

    def remove_game_change_listener(self, to_be_deleted) -> bool:
        for handler in self._handlers:
            if handler == to_be_deleted:
                self._handlers.remove(handler)
                return True
        else:
            logger.info(f"Error: {to_be_deleted} not in game handlers.")
            return False

    def _move(self, steps: int) -> Optional[Land]:
        cur_player = self.cur_player
        new_position = (cur_player.position + steps) % len(self._board)
        if new_position != 0 and new_position <= cur_player.position:
            # A new round
            cur_player.add_money(START_REWARD)
            self.notify_pass_start()
        land_dest = self._board.land_at(new_position)
        # assert (land_dest is not None)
        if land_dest is None:
            self.notify_error("Error: Destination land is None. There is no land at the new position.")
            return None
        cur_player.position = new_position
        return land_dest

    def _is_purchase_affordable(self, land: Union[Constructable, Infrastructure]):
        return self.cur_player.money >= land.price

    def _is_construction_affordable(self, land: Constructable):
        return self.cur_player.money >= land.construction_price

    def _generate_move_receipt(self, land: Land) -> MoveReceipt:
        land_type = land.type
        if land_type == LandType.CONSTRUCTABLE:
            self._move_receipt = MoveReceipt.handle_construction(self.cur_player, land)
        elif land_type == LandType.INFRASTRUCTURE:
            self._move_receipt = MoveReceipt.handle_infrastructure(self.cur_player, land)
        elif land_type == LandType.PARKING:
            self._move_receipt = MoveReceipt(MoveReceiptType.NOTHING, 0, land)
        elif land_type == LandType.JAIL:
            self._move_receipt = MoveReceipt(MoveReceiptType.STOP_ROUND, 0, land)
        elif land_type == LandType.CHANCE:
            card = self._card_deck.draw()
            if card.money_deduction > 0:
                result_type = MoveReceiptType.PAYMENT
                val = card.money_deduction
            else:
                result_type = MoveReceiptType.REWARD
                val = -1 * card.money_deduction
            self._move_receipt = MoveReceipt(result_type, val, land)
            self._move_receipt.msg = "Chance Card: " + str(card)
        elif land_type == LandType.START:
            self._move_receipt = MoveReceipt(MoveReceiptType.REWARD, START_REWARD, land)
        return self._move_receipt

    def _apply_move_receipt_option(self, move_result: MoveReceipt) -> bool:
        move_result_type = move_result.type
        if not move_result.option:  # user choose no
            return True

        if move_result_type == MoveReceiptType.BUY_LAND_OPTION:
            purchasable_land: Union[Constructable, Infrastructure] = move_result.land.content
            if not self._is_purchase_affordable(purchasable_land):
                self.notify_error("Error: No enough money to buy the property.")
                return False
            result = move_result.apply_buy(self.cur_player)
            return result
        elif move_result_type == MoveReceiptType.CONSTRUCTION_OPTION:
            construction_land: Constructable = move_result.land.content
            if not self._is_construction_affordable(construction_land):
                self.notify_error("Error: No enough money to construct new property.")
                return False
            result, error = move_result.apply_construction(self.cur_player)
            if error:
                self.notify_error(error)
            return result

    def _apply_move_receipt_none_option(self, decision: MoveReceipt) -> bool:
        move_result_type = decision.type
        val = decision.value
        if move_result_type == MoveReceiptType.PAYMENT:
            self.cur_player.deduct_money(val)
            if self.cur_player.money < 0:
                self.notify_game_ended()
                self.game_state = GameStateType.GAME_ENDED
                return False
            content = decision.land.content
            if content.type in [LandType.CONSTRUCTABLE, LandType.INFRASTRUCTURE]:
                # this is the payment to the player
                if content.owner is None:
                    self.notify_error(f"Error: The land:{decision.land}, content:{content} has no owner.")
                    return False
                # assert land.get_owner_index() is not None
                logger.info(f'[land:{decision.land}, content: {content}, owner: {content.owner}]')
                rewarded_player: Player = content.owner
                rewarded_player.add_money(val)
        elif move_result_type == MoveReceiptType.REWARD:
            self.cur_player.add_money(val)
        elif move_result_type == MoveReceiptType.STOP_ROUND:
            self.cur_player.add_one_stop()
        else:
            pass
        self.notify_move_result_applied(decision)
        return True

    def execute_move_receipt(self, decision: MoveReceipt) -> Optional[MoveReceipt]:
        if not self.assert_before(GameStateType.WAIT_FOR_DECISION):
            return None
        # assert self.status() == GameStateType.WAIT_FOR_DECISION
        self.notify_decision_made(decision)
        if decision.type not in [MoveReceiptType.BUY_LAND_OPTION, MoveReceiptType.CONSTRUCTION_OPTION]:
            logger.info("decision move result: 'PAYMENT' or 'REWARD' or 'STOP_ROUND' or 'NOTHING'")
            is_success = self._apply_move_receipt_none_option(decision)
        else:  # decision is option
            if decision.option is None:
                self.notify_error(f"Error: You must choose option to decision {decision}.")
                return MoveReceipt(MoveReceiptType.NOTHING, 0, decision.land)
            is_success = self._apply_move_receipt_option(decision)

        if is_success:
            logger.info(f'decision {decision} is made and applied successfully')
            self._change_player()
            self._to_next_game_state()
            return self._move_receipt
        else:  # cannot affordable
            return MoveReceipt(MoveReceiptType.NOTHING, 0, decision.land)

    def _to_next_game_state(self):
        self.game_state = 1 - self.game_state

    def assert_before(self, state) -> bool:
        if self.game_state == GameStateType.GAME_ENDED:
            self.notify_error("Internal error: the game has ended")
            return False
        if self.game_state != state:
            self.notify_error("Internal error: the game state must be 'waiting for roll' when you roll")
            return False
        return True

    def roll(self, steps: int = None) -> (int, MoveReceipt):
        if not self.assert_before(GameStateType.WAIT_FOR_ROLL):
            return None
        # assert self.status() == GameStateType.WAIT_FOR_ROLL
        self.notify_rolled()

        steps = self._dice.roll(steps)
        land_dest = self._move(steps)
        if land_dest is None:
            return None
        logger.info(f"land destination: {land_dest}")
        self._to_next_game_state()
        move_result = self._generate_move_receipt(land_dest)
        return steps, move_result

    # this will return a 40 num array, each indicate the owner of each land
    def get_land_owners(self):
        ret = []
        for i in range(len(self._board)):
            land = self._board.land_at(i)
            owner = land.content.owner
            ret.append(owner)
        return ret

    # notifications
    def notify_new_game(self):
        for handler in self._handlers:
            handler.on_new_game()

    def notify_game_ended(self):
        for handler in self._handlers:
            handler.on_game_ended()

    def notify_rolled(self):
        for handler in self._handlers:
            handler.on_rolled()

    def notify_player_changed(self):
        for handler in self._handlers:
            handler.on_player_changed()

    def notify_decision_made(self, mr):
        for handler in self._handlers:
            handler.on_decision_made(mr)

    def notify_move_result_applied(self, mr):
        for handler in self._handlers:
            handler.on_receipt_applied(mr)

    def notify_error(self, err_msg):
        for handler in self._handlers:
            handler.on_error(err_msg)

    def notify_pass_start(self):
        for handler in self._handlers:
            handler.on_pass_start()
