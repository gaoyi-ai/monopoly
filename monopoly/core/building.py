RATIO_RENT_TO_PRICE_FOR_HOUSE = 4
RATIO_RENT_TO_PRICE_FOR_HOTEL = 2

HOTEL_CONSTRUCTION_COST = 150
HOUSE_CONSTRUCTION_COST = 100

START_REWARD = 200


class BuildingType:
    HOUSE = 0
    HOTEL = 1
    NOTHING = 2


class Building:

    def __init__(self, id, land_index, building_type, price, description, owner):
        self.id = id
        self.land_index = land_index
        self.type = building_type
        self.price = price
        self.description = description
        self.owner = owner

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id

    def __ne__(self, other):
        return not self.__eq__(other)
