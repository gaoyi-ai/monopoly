class RoomStatus:
    WAITING = 0
    GAMING = 1
    FULL = 2


class Room:

    def __init__(self, host) -> None:
        self.players = set()
        self.host = host
        self.status = RoomStatus.WAITING

    def join(self, player):
        if self._check():
            self.players.add(player)

    def _check(self):
        if self.__len__() >= 4:
            self.status = RoomStatus.FULL
            return False
        return True

    def __len__(self):
        return len(self.players)

    def __str__(self):
        return f"Room {self.host} with {self.players} in {self.status}"

    def __repr__(self):
        return self.players
