import logging

logger = logging.getLogger(__name__)

START_REWARD = 200


class LandType:
    CONSTRUCTABLE = 0
    INFRASTRUCTURE = 1
    START = 2
    PARKING = 3
    JAIL = 4
    CHANCE = 5

    @staticmethod
    def description(val):
        ret = ["Constructable",
               "Infrastructure",
               "New Start",
               "Parking ",
               "AIV Jail",
               "Chance Card"]
        return ret[val]


class Land:

    def __init__(self, pos, description, content):
        self.pos = pos
        self.description = description
        self.content = content

    @property
    def type(self):
        return self.content.type

    def evaluate(self):
        if self.type in [LandType.INFRASTRUCTURE, LandType.CONSTRUCTABLE]:
            return self.content.valuation
        return 0

    def __str__(self):
        return f"[position: {self.pos}, content type: {LandType.description(self.type)}]"


class BuildingType:
    HOUSE = 0
    HOTEL = 1
    NOTHING = 2


class Constructable:
    RATIO_RENT_TO_PRICE_NOTHING = 5
    RATIO_RENT_TO_PRICE_FOR_HOUSE = 4
    RATIO_RENT_TO_PRICE_FOR_HOTEL = 2

    HOTEL_CONSTRUCTION_COST = 150
    HOUSE_CONSTRUCTION_COST = 100

    def __init__(self, price):
        self.price = price
        self.property_type = BuildingType.NOTHING
        self.building_num = 0
        self.owner = None

    @property
    def valuation(self):
        building_value = self.price
        if self.property_type == BuildingType.HOUSE:
            building_value += Constructable.HOUSE_CONSTRUCTION_COST * self.building_num
        elif self.property_type == BuildingType.HOTEL:
            building_value += Constructable.HOUSE_CONSTRUCTION_COST * 3 + Constructable.HOTEL_CONSTRUCTION_COST
        return building_value

    @property
    def toll(self):
        if self.property_type == BuildingType.NOTHING:
            rent = self.price / Constructable.RATIO_RENT_TO_PRICE_NOTHING
        elif self.property_type == BuildingType.HOTEL:
            rent = (self.price + Constructable.HOTEL_CONSTRUCTION_COST) / Constructable.RATIO_RENT_TO_PRICE_FOR_HOTEL
        else:
            rent = (self.price + self.building_num * Constructable.HOUSE_CONSTRUCTION_COST) / \
                   Constructable.RATIO_RENT_TO_PRICE_FOR_HOUSE
        logger.info(f"[Constructable: {self}, toll: {rent}]")
        return rent

    @property
    def type(self):
        return LandType.CONSTRUCTABLE

    @property
    def construction_price(self):
        return Constructable.HOTEL_CONSTRUCTION_COST \
            if self.property_type == BuildingType.HOUSE and self.building_num == 3 \
            else Constructable.HOUSE_CONSTRUCTION_COST

    def clear_properties(self):
        self.property_type = BuildingType.NOTHING
        self.building_num = 0

    def is_constructable(self):
        return not self.property_type == BuildingType.HOTEL

    def incr_property(self) -> bool:
        if self.property_type == BuildingType.NOTHING or \
                (self.property_type == BuildingType.HOUSE and
                 self.building_num < 3):
            self.building_num += 1
            self.property_type = BuildingType.HOUSE
            return True
        elif self.property_type == BuildingType.HOUSE and self.building_num == 3:
            self.property_type = BuildingType.HOTEL
            self.building_num = 1
            return True
        elif self.property_type == BuildingType.HOTEL:
            return False


class Infrastructure:

    def __init__(self, price):
        self.price = price
        self.owner = None

    @property
    def type(self):
        return LandType.INFRASTRUCTURE

    @property
    def payment(self):
        return self.price / 4

    @property
    def valuation(self):
        return self.price


class OwnRejection:
    @property
    def owner(self):
        return None


class Start(OwnRejection):

    def __init__(self, reward):
        self.reward = reward

    @property
    def type(self):
        return LandType.START


class Jail(OwnRejection):

    def __init__(self, stops: int):
        self.stops = stops

    @property
    def type(self):
        return LandType.JAIL


class Parking(OwnRejection):

    @property
    def type(self):
        return LandType.PARKING


class Chance(OwnRejection):

    @property
    def type(self):
        return LandType.CHANCE
