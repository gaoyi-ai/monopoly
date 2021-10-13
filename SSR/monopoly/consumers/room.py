import json.tool


class RoomStatus:
    WAITING = 0
    GAMING = 1
    FULL = 2

    @staticmethod
    def description(val):
        ret = ["WAITING",
               "GAMING",
               "FULL", ]
        return ret[val]


class Room:

    def __init__(self, host) -> None:
        self.players = set()
        self.host = host
        self.status = RoomStatus.WAITING

    def join(self, player):
        if self._check():
            self.players.add(player)

    def _check(self):
        if self.__len__() >= 8:
            self.status = RoomStatus.FULL
            return False
        return True

    def __len__(self):
        return len(self.players)

    def __str__(self):
        return f"Room {self.host} with {self.players} in {RoomStatus.description(self.status)}"

    def __repr__(self):
        return {"host": self.host, "players": list(self.players), "status": RoomStatus.description(self.status)}

    def to_json(self):
        return str(self.__repr__())
