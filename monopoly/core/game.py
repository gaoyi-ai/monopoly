from monopoly.core.card_deck import CardDeck
from monopoly.core.land import LandType
from monopoly.core.board import Board
from monopoly.core.building import START_REWARD
from monopoly.core.move_result import MoveResult, MoveResultType
from monopoly.core.player import Player
from monopoly.core.util import InternalLogHandler

import logging

logger = logging.getLogger(__name__)


class GameStateType:
    WAIT_FOR_ROLL = 0
    WAIT_FOR_DECISION = 1
    GAME_ENDED = 2


class Game:
    _game_id = 0

    def __init__(self, player_num):
        # assert 0 < player_num <= 4
        if player_num <= 0 or player_num > 4:
            self.notify_error("In correct player number, should be 1-4 players.")
            return
        self._players = [Player(i) for i in range(player_num)]
        self._game_state = GameStateType.WAIT_FOR_ROLL
        self._card_deck = CardDeck()
        self._board = Board()
        self._current_player_index = 0
        self._game_id = Game._game_id
        Game._game_id += 1
        self._handlers = []
        self.add_game_change_listener(InternalLogHandler(self))
        self.notify_new_game()

    def get_game_id(self):
        return self._game_id

    def add_game_change_listener(self, handler):
        self._handlers.append(handler)

    def remove_game_change_listener(self, to_be_deleted):
        for handler in self._handlers:
            if handler == to_be_deleted:
                self._handlers.remove(handler)
                return

    def _move(self, steps: int):
        cur_player = self.get_current_player()
        new_position = (cur_player.get_position() + steps) % self._board.get_grid_num()
        if new_position < cur_player.get_position():
            # A new round
            self.get_current_player().add_money(START_REWARD)
            self.notify_pass_start()
        land_dest = self._board.get_land(new_position)
        # assert (land_dest is not None)
        if land_dest is None:
            self.notify_error("Internal error, the destination land is none. There is no land at the new position")
            return None
        self.get_current_player().set_position(new_position)
        return land_dest

    def _is_purchase_affordable(self, land):
        return self.get_current_player().get_money() >= land.get_price()

    def _is_construction_affordable(self, land):
        return self.get_current_player().get_money() >= land.get_next_construction_price()

    def _move_result_CONSTRUCTION(self, land):
        construction_land = land.get_content()
        if construction_land.get_owner_index() is None:  # land is none owned
            price = construction_land.get_price()
            if self._is_purchase_affordable(construction_land) is False:
                return MoveResult(MoveResultType.NOTHING, price, land)

            return MoveResult(MoveResultType.BUY_LAND_OPTION, price, land)
        elif construction_land.get_owner_index() == self._current_player_index:  # land is owned by self
            if construction_land.is_constructable() is False:
                return MoveResult(MoveResultType.NOTHING, 0, land)
            price = construction_land.get_next_construction_price()
            if self._is_construction_affordable(construction_land) is False:
                return MoveResult(MoveResultType.NOTHING, price, land)

            return MoveResult(MoveResultType.CONSTRUCTION_OPTION, price, land)
        else:  # land is owned
            rent = construction_land.get_rent()
            return MoveResult(MoveResultType.PAYMENT, rent, land)

    def _move_result_INFRA(self, land):
        infra_land = land.get_content()
        if infra_land.get_owner_index() is None:
            price = infra_land.get_price()
            if self._is_purchase_affordable(infra_land) is False:
                return MoveResult(MoveResultType.NOTHING, price, land)
            return MoveResult(MoveResultType.BUY_LAND_OPTION, price, land)
        else:
            if infra_land.get_owner_index() == self._current_player_index:
                return MoveResult(MoveResultType.NOTHING, 0, land)
            payment = infra_land.get_payment()
            return MoveResult(MoveResultType.PAYMENT, payment, land)

    def _get_move_result(self, land) -> MoveResult:
        land_type = land.get_type()
        if land_type == LandType.CONSTRUCTION_LAND:
            return self._move_result_CONSTRUCTION(land)
        elif land_type == LandType.INFRA:
            return self._move_result_INFRA(land)

        elif land_type == LandType.START:
            return MoveResult(MoveResultType.REWARD, START_REWARD, land)
        elif land_type == LandType.PARKING:
            return MoveResult(MoveResultType.NOTHING, 0, land)
        elif land_type == LandType.JAIL:
            return MoveResult(MoveResultType.STOP_ROUND, 1, land)
        elif land_type == LandType.CHANCE:
            card = self._card_deck.draw()
            if card.get_money_deduction() > 0:
                result_type = MoveResultType.PAYMENT
                val = card.get_money_deduction()
            else:
                result_type = MoveResultType.REWARD
                val = card.get_money_deduction() * -1
            ret = MoveResult(result_type, val, land)
            ret.set_msg(" Chance Card: " + str(card))
            return ret
        else:
            logger.error("Error, the land is", land_type)
            self.notify_error("Internal error, unknown land type")
            return None

    def _has_enough_money(self, construction_land):
        logger.info(f'player: {self.get_current_player()} money: {self.get_current_player().get_money()}')
        logger.info('construction price:', construction_land.get_price())
        return self.get_current_player().get_money() > construction_land.get_price()

    def _apply_move_result_BUY_LAND(self, move_result: MoveResult):
        purchasable_land = move_result.get_land().get_content()
        if move_result.is_confirmed() is True:
            if not self._has_enough_money(purchasable_land):
                self.notify_error("No enough money to buy the property.")
                return False
            purchasable_land.set_owner(self._current_player_index)
            self.get_current_player().add_properties(purchasable_land)
            self.get_current_player().deduct_money(purchasable_land.get_price())
        return True

    def _apply_move_result_CONSTRUCTION(self, move_result: MoveResult):
        construction_land = move_result.get_land().get_content()
        if construction_land.get_owner_index() != self._current_player_index:
            self.notify_error("Error. This land is not owned by the current player, cannot make construction.")
            return False
        # assert construction_land.get_owner_index() == self._current_player_index
        if move_result.is_confirmed() is True:
            self.get_current_player().deduct_money(construction_land.get_next_construction_price())
            if construction_land.add_properties() is False:
                self.notify_error("Error. Add property fail. ")
                return False
        return True

    def _apply_move_result(self, move_result: MoveResult) -> bool:
        move_result_type = move_result.get_move_result_type()
        val = move_result.get_value()
        result = True
        if move_result_type == MoveResultType.BUY_LAND_OPTION:
            result = self._apply_move_result_BUY_LAND(move_result)
        elif move_result_type == MoveResultType.CONSTRUCTION_OPTION:
            result = self._apply_move_result_CONSTRUCTION(move_result)
        else:
            if move_result_type == MoveResultType.PAYMENT:
                self.get_current_player().deduct_money(val)
                if self.get_current_player().get_money() < 0:
                    self.notify_game_ended()
                    self._game_state = GameStateType.GAME_ENDED
                land = move_result.get_land().get_content()
                if land.get_type() == LandType.CONSTRUCTION_LAND or land.get_type() == LandType.INFRA:
                    # this is the payment to the player
                    if land.get_owner_index() is None:
                        self.notify_error("Error: The land has no owner. why the current player need to make payment")
                        result = False
                    # assert land.get_owner_index() is not None
                    logger.info(f'owner index is: {land.get_owner_index()}')
                    rewarded_player = self.get_player(land.get_owner_index())
                    rewarded_player.add_money(val)

            elif move_result_type == MoveResultType.REWARD:
                self.get_current_player().add_money(val)

            elif move_result_type == MoveResultType.STOP_ROUND:
                self.get_current_player().add_one_stop()

            self.notify_move_result_applied()

        return result

    def _change_player(self):
        self._current_player_index = self._change_player_on(self._current_player_index)
        self.notify_player_changed()

    def _change_player_on(self, cur):
        new_user_index = (cur + 1) % (len(self._players))
        logger.info(f"new_user_index: {new_user_index}")
        new_user = self._players[new_user_index]
        if new_user.get_stop_num() > 0:  # the next player is in stopping
            new_user.deduct_stop_num()
            return self._change_player_on(new_user_index)
        else:
            return new_user_index

    def _roll_to_next_game_state(self):
        self._game_state = 1 - self._game_state

    def roll(self, steps: int = None) -> (int, MoveResult):
        if self.get_game_status() == GameStateType.GAME_ENDED:
            self.notify_error("Internal error: the game has ended")
            return None
        if self.get_game_status() != GameStateType.WAIT_FOR_ROLL:
            self.notify_error("Internal error: the game state must be 'waiting for roll' when you roll")
            return None
        # assert self.get_game_status() == GameStateType.WAIT_FOR_ROLL
        self.notify_rolled()

        if steps is None:
            import random
            steps1 = random.randint(1, 6)
            steps2 = random.randint(1, 6)
            steps = steps1 + steps2
        land_dest = self._move(steps)
        if land_dest is None:
            logger.info("Internal error, the destination land is none. There is no land at the new position")
            return None
        logger.info(f"land destination:{land_dest}")
        self._roll_to_next_game_state()
        move_result = self._get_move_result(land_dest)
        return steps, move_result

    def make_decision(self, decision: MoveResult):
        if self.get_game_status() == GameStateType.GAME_ENDED:
            self.notify_error("Internal error: the game has ended")
            return None
        if self.get_game_status() != GameStateType.WAIT_FOR_DECISION:
            self.notify_error("Internal error: the game state must be "
                              "'waiting for decision when you make decision'")
            return None
        # assert self.get_game_status() == GameStateType.WAIT_FOR_DECISION
        self.notify_decision_made()
        ret = decision
        if decision.move_result_type != MoveResultType.BUY_LAND_OPTION and \
                decision.move_result_type != MoveResultType.CONSTRUCTION_OPTION:
            logger.info(f"decision move result: {MoveResultType.PAYMENT} or {MoveResultType.REWARD} "
                        f"or {MoveResultType.STOP_ROUND} or {MoveResultType.NOTHING}")
            is_success = self._apply_move_result(decision)
        else:  # decision is option
            if decision.is_confirmed() is None:
                self.notify_error("Error: You must confirm when you need to make a decision and apply it.")
                return None
            is_success = self._apply_move_result(decision)
            ret = MoveResult(decision.get_move_result_type(),
                             decision.get_value(), decision.get_land())

        if is_success:
            logger.info('decision is made and applied successfully')
            self._change_player()
            self._roll_to_next_game_state()
            return ret
        else:
            return None

    def get_player(self, index):
        return self._players[index]

    # this will return a 40 num array, each indicate the owner of each land
    def get_land_owners(self):
        ret = []
        for i in range(self._board.get_grid_num()):
            land = self._board.get_land(i)
            owner = land.get_content().get_owner_index()
            ret.append(owner)
        return ret

    def get_current_player(self):
        return self._players[self._current_player_index]

    def get_land(self, index):
        return self._board.get_land(index)

    def get_players(self):
        return self._players

    def get_game_status(self):
        return self._game_state

    # get the total status of the current game
    # return: return a 4 element tuple: dict(players, board, current_player_index,game_state)
    def get_status(self):
        return {'players': self.get_players(), 'board': self._board,
                'cur player index': self._current_player_index, 'game status': self.get_game_status()}

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

    def notify_decision_made(self):
        for handler in self._handlers:
            handler.on_decision_made()

    def notify_move_result_applied(self):
        for handler in self._handlers:
            handler.on_result_applied()

    def notify_error(self, err_msg):
        for handler in self._handlers:
            handler.on_error(err_msg)

    def notify_pass_start(self):
        for handler in self._handlers:
            handler.on_pass_start()
