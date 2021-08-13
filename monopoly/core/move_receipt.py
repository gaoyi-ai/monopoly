from typing import Optional

from monopoly.core.land import Land, Constructable, Infrastructure
from monopoly.core.player import Player

import logging

logger = logging.getLogger(__name__)


class ModalTitleType:
    @staticmethod
    def description(val):
        ret = ["Purchase Land",
               "Make a Payment",
               "Get Reward",
               "Stop One Round",
               "Build a House",
               "Nothing actually happened"]
        return ret[val]


class MoveReceiptType:
    BUY_LAND_OPTION = 0
    PAYMENT = 1
    REWARD = 2
    STOP_ROUND = 3
    CONSTRUCTION_OPTION = 4
    NOTHING = 5

    @staticmethod
    def description(val):
        ret = ["Now choosing to buy or not.",
               "Now should make a payment.",
               "Now reward a fortune.",
               "Now stopped for one round.",
               "Now choosing to build a new building or not.",
               "Nothing actually happened."]
        return ret[val]


class MoveReceipt:

    def __init__(self, move_result_type, value, land):
        self.type = move_result_type
        self.value = value
        self.land = land
        self._option = None  # user choice
        self.msg = None

    @property
    def option(self):
        return self._option

    @option.setter
    def option(self, choice):
        if self._is_option():
            self._option = choice
        else:
            logger.error("Error: Cannot make a decision because it can not be chosen.")

    def _is_option(self):
        return self.type == MoveReceiptType.BUY_LAND_OPTION or \
               self.type == MoveReceiptType.CONSTRUCTION_OPTION

    @staticmethod
    def handle_construction(player, land: Land):
        construction: Constructable = land.content
        if construction.owner is None:  # land is none owned
            price = construction.price
            return MoveReceipt(MoveReceiptType.BUY_LAND_OPTION, price, land)

        elif construction.owner is player:  # land is owned by self
            if not construction.is_constructable():
                return MoveReceipt(MoveReceiptType.NOTHING, 0, land)
            price = construction.construction_price
            return MoveReceipt(MoveReceiptType.CONSTRUCTION_OPTION, price, land)
        else:  # owned by others
            rent = construction.toll
            return MoveReceipt(MoveReceiptType.PAYMENT, rent, land)

    @staticmethod
    def handle_infrastructure(player, land: Land):
        infrastructure: Infrastructure = land.content
        if infrastructure.owner is None:
            price = infrastructure.price
            return MoveReceipt(MoveReceiptType.BUY_LAND_OPTION, price, land)
        else:
            if infrastructure.owner is player:
                return MoveReceipt(MoveReceiptType.NOTHING, 0, land)
            payment = infrastructure.payment
            return MoveReceipt(MoveReceiptType.PAYMENT, payment, land)

    def apply_buy(self, player: Player):
        purchasable: Optional[Constructable, Infrastructure] = self.land.content
        purchasable.owner = player
        player.add_property(purchasable)
        player.deduct_money(self.value)
        return True

    def apply_construction(self, player: Player):
        construction: Constructable = self.land.content
        if construction.owner is not player:
            return False, f"Error: This land is not owned by {player}, cannot make construction."
        # assert construction.get_owner_index() == self._current_player_index
        if not construction.incr_property():
            return False, "Error: Add property fail."
        player.deduct_money(self.value)
        return True, None

    def __repr__(self):
        return f"Move Receipt [" \
               f"type: {MoveReceiptType.description(self.type)}. " \
               f"value: {self.value}, " \
               f"land: {self.land}, " \
               f"option: {self.option}, " \
               f"msg: {self.msg}]"

    def __str__(self):
        return self.__repr__()

    def beautify(self):
        saying = self.msg if self.msg else ""
        saying += " " + MoveReceiptType.description(self.type)
        if self.type == MoveReceiptType.BUY_LAND_OPTION:
            saying += "The price is " + str(self.value)
        elif self.type == MoveReceiptType.PAYMENT:
            saying += "The payment amount is " + str(self.value)
        elif self.type == MoveReceiptType.REWARD:
            saying += "The award amount is " + str(self.value)
        elif self.type == MoveReceiptType.STOP_ROUND:
            pass
        elif self.type == MoveReceiptType.CONSTRUCTION_OPTION:
            saying += "The cost for the building is " + str(self.value)
        else:  # Nothing
            pass
        return saying
