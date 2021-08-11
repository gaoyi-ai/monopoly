from typing import Optional

from monopoly.core.land import Land, Constructable, Infrastructure
from monopoly.core.player import Player


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
        ret = ["is choosing to buy or not. ",
               "should make a payment. ",
               "is rewarded a fortune. ",
               "is stopped for one round. ",
               "is choosing to build a new building or not. ",
               "Nothing actually happened. "]
        return ret[val]


class MoveReceipt:

    def __init__(self, move_result_type, value, land):
        self.type = move_result_type
        self.value = value
        self.land = land
        self.confirmed = None
        self.msg = None

    def confirm(self, confirm):
        if self.is_option():
            self.confirmed = confirm

    def is_option(self):
        return self.type == MoveReceiptType.BUY_LAND_OPTION or \
               self.type == MoveReceiptType.CONSTRUCTION_OPTION

    @staticmethod
    def handle_construction(player, land: Land, is_affordable: bool):
        construction: Constructable = land.content
        if construction.owner is None:  # land is none owned
            price = construction.price
            return MoveReceipt(MoveReceiptType.BUY_LAND_OPTION, price, land) \
                if is_affordable \
                else MoveReceipt(MoveReceiptType.NOTHING, price, land)

        elif construction.owner == player:  # land is owned by self
            if not construction.is_constructable():
                return MoveReceipt(MoveReceiptType.NOTHING, 0, land)
            price = construction.next_construction_price()
            return MoveReceipt(MoveReceiptType.CONSTRUCTION_OPTION, price, land) \
                if is_affordable \
                else MoveReceipt(MoveReceiptType.NOTHING, price, land)
        else:  # owned by others
            rent = construction.rent()
            return MoveReceipt(MoveReceiptType.PAYMENT, rent, land)

    @staticmethod
    def handle_infrastructure(player, land: Land, is_affordable: bool):
        infrastructure: Infrastructure = land.content
        if infrastructure.owner is None:
            price = infrastructure.price
            return MoveReceipt(MoveReceiptType.BUY_LAND_OPTION, price, land) \
                if is_affordable \
                else MoveReceipt(MoveReceiptType.NOTHING, price, land)
        else:
            if infrastructure.owner == player:
                return MoveReceipt(MoveReceiptType.NOTHING, 0, land)
            payment = infrastructure.payment
            return MoveReceipt(MoveReceiptType.PAYMENT, payment, land)

    def apply_buy(self, player: Player):
        purchasable: Optional[Constructable, Infrastructure] = self.land.content
        if self.confirmed is True:
            purchasable.owner = player
            player.add_property(purchasable)
            player.deduct_money(purchasable.price)
            return True, None
        return False, f"Error: Move result {self} not confirmed."

    def apply_construction(self, player: Player):
        construction: Constructable = self.land.content
        if construction.owner != player:
            return False, f"Error: This land is not owned by {player}, cannot make construction."
        # assert construction.get_owner_index() == self._current_player_index
        if self.confirmed is True:
            if construction.incr_property() is False:
                return False, "Error: Add property fail."
            player.deduct_money(construction.next_construction_price())
            return True, None
        return False, f"Error: Move result {self} not confirmed."

    def __str__(self):
        saying = self.msg if self.msg else ""
        saying += MoveReceiptType.description(self.type)
        ret = saying + f" value:{self.value}, land: {self.land}"
        if self.confirmed is not None:
            ret += f" decision: {self.confirmed}"
        return ret

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
        else:
            pass

        return saying
