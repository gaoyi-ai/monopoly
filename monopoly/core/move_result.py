from monopoly.core.land import Land


class ModalTitleType:
    @staticmethod
    def get_description(val):
        ret = ["Purchase Land",
               "Make a Payment",
               "Get Reward",
               "Stop One Round",
               "Build a House",
               "Nothing actually happened"]
        return ret[val]


class MoveResultType:
    BUY_LAND_OPTION = 0
    PAYMENT = 1
    REWARD = 2
    STOP_ROUND = 3
    CONSTRUCTION_OPTION = 4
    NOTHING = 5

    @staticmethod
    def get_description(val):
        ret = ["is choosing to buy or not. ",
               "should make a payment. ",
               "is rewarded a fortune. ",
               "is stopped for one round. ",
               "is choosing to build a new building or not. ",
               "Nothing actually happened. "]
        return ret[val]


class MoveResult:

    def __init__(self, move_result_type, value, land):
        self.move_result_type = move_result_type
        self.value = value
        self.land = land
        self._confirmed = None
        self.msg = None

    def set_msg(self, msg):
        self.msg = msg

    def get_move_result_type(self):
        return self.move_result_type

    def get_value(self):
        return self.value

    def get_land(self) -> Land:
        return self.land

    def confirm(self, confirm):
        if self.is_option():
            self._confirmed = confirm

    def is_confirmed(self):
        return self._confirmed

    def is_option(self):
        return self.move_result_type == MoveResultType.BUY_LAND_OPTION or \
               self.move_result_type == MoveResultType.CONSTRUCTION_OPTION

    def __str__(self):
        saying = self.msg if self.msg else ""
        saying += MoveResultType.get_description(self.move_result_type)
        ret = saying + f" value:{self.value}, land: {self.land}"
        if self._confirmed is not None:
            ret += f" decision: {self._confirmed}"
        return ret

    def beautify(self):
        saying = self.msg if self.msg else ""
        saying += " " + MoveResultType.get_description(self.move_result_type)
        if self.move_result_type == MoveResultType.BUY_LAND_OPTION:
            saying += "The price is " + str(self.value)
        elif self.move_result_type == MoveResultType.PAYMENT:
            saying += "The payment amount is " + str(self.value)
        elif self.move_result_type == MoveResultType.REWARD:
            saying += "The award amount is " + str(self.value)
        elif self.move_result_type == MoveResultType.STOP_ROUND:
            pass
        elif self.move_result_type == MoveResultType.CONSTRUCTION_OPTION:
            saying += "The cost for the building is " + str(self.value)
        else:
            pass

        return saying
