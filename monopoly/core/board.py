from monopoly.core.building import START_REWARD
from monopoly.core.land import *


class Board:

    def __init__(self):
        self.lands = []
        self._generate_lands()

    def land_at(self, index: int) -> Land:
        return self.lands[index]

    def _generate_lands(self):
        self.lands.append(Land(0, "Start", Start(START_REWARD)))
        self.lands.append(Land(1, "Warner Hall", Constructable(60)))
        self.lands.append(Land(2, "Chance", Chance()))
        self.lands.append(Land(3, "UC", Constructable(60)))
        self.lands.append(Land(4, "Union Grill", Infrastructure(150)))
        self.lands.append(Land(5, "AB route", Infrastructure(200)))
        self.lands.append(Land(6, "College of Fine Art", Constructable(100)))
        self.lands.append(Land(7, "Chance", Chance()))
        self.lands.append(Land(8, "Posner Hall", Constructable(100)))
        self.lands.append(Land(9, "Hunt Library", Constructable(120)))
        self.lands.append(Land(10, "AIV Jail", Jail(1)))
        self.lands.append(Land(11, "Doherty Hall", Constructable(140)))
        self.lands.append(Land(12, "Entropy+", Infrastructure(150)))
        self.lands.append(Land(13, "Gasling Stadium", Constructable(140)))
        self.lands.append(Land(14, "Margaret Morrison Carnegie Hall", Constructable(160)))
        self.lands.append(Land(15, "Escort", Infrastructure(200)))
        self.lands.append(Land(16, "Hamerschlag Hall", Constructable(180)))
        self.lands.append(Land(17, "Chance", Chance()))
        self.lands.append(Land(18, "Roberts Engineering Hall", Constructable(180)))
        self.lands.append(Land(19, "Porter Hall", Constructable(200)))
        self.lands.append(Land(20, "Parking", Parking()))
        self.lands.append(Land(21, "Gates Center", Constructable(220)))
        self.lands.append(Land(22, "Chance", Chance()))
        self.lands.append(Land(23, "Newell-Simon Hall", Constructable(220)))
        self.lands.append(Land(24, "Wean Hall", Constructable(240)))
        self.lands.append(Land(25, "PTC", Infrastructure(200)))
        self.lands.append(Land(26, "Baker Hall", Constructable(260)))
        self.lands.append(Land(27, "Fence", Constructable(260)))
        self.lands.append(Land(28, "iNoodle", Infrastructure(150)))
        self.lands.append(Land(29, "Purnell Center", Constructable(280)))
        self.lands.append(Land(30, "AIV Jail", Jail(1)))
        self.lands.append(Land(31, "Hamburg Hall", Constructable(300)))
        self.lands.append(Land(32, "Collaborative Innovation Center", Constructable(300)))
        self.lands.append(Land(33, "Chance", Chance()))
        self.lands.append(Land(34, "Cyert Hall", Constructable(320)))
        self.lands.append(Land(35, "Monorail", Infrastructure(200)))
        self.lands.append(Land(36, "Chance", Chance()))
        self.lands.append(Land(37, "Information Networking Institute", Constructable(350)))
        self.lands.append(Land(38, "Pasta Vilaggio", Infrastructure(150)))
        self.lands.append(Land(39, "Mellon Institute", Constructable(400)))

    def __len__(self):
        return len(self.lands)
