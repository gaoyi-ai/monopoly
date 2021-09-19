from monopoly.core.land import Land

INIT_PLAYER_MONEY = 1500


class Player:

    def __init__(self, index):
        self.index = index
        self.money = INIT_PLAYER_MONEY
        self.position = 0
        self.remaining_stop = 0  # 等待回合数
        self.properties = set()

    def add_property(self, land: Land):
        self.properties.add(land)

    def assets_evaluation(self):
        ret = self.money
        for land in self.properties:
            ret += land.evaluate()
        return self.money
        # return ret

    def remove_property(self, building):
        self.properties.remove(building)

    def add_money(self, val):
        self.money += val

    def deduct_money(self, val):
        self.money -= val

    def set_stop(self, val):
        self.remaining_stop = val

    def add_stop(self, val):
        self.remaining_stop += val

    def add_one_stop(self):
        self.add_stop(1)

    def deduct_stop(self, val):
        self.add_stop(-1 * val)

    def __str__(self):
        return f"Player index: {self.index}"
