from random import shuffle

from monopoly.core.card import Card


class CardDeck:

    def __init__(self):
        self.cur_index = 0
        self.cards = []
        self._init_cards()

    def __len__(self):
        return len(self.cards)

    def _init_cards(self):
        self.cards.append(Card("Get One More Grace day", 100, 0))
        self.cards.append(Card("Overspeed ", 200, 0))
        self.cards.append(Card("Autolab rank reward ", -100, 0))
        self.cards.append(Card("Illegal Parking ", 150, 0))
        self.cards.append(Card("Meet harry potter in Doherty Hall", -150, 0))
        self.cards.append(Card("Host a fantastic Carnival", -200, 0))
        self.shuffle()

    def insert(self, card: Card):
        self.cards.append(card)

    def shuffle(self):
        shuffle(self.cards)

    def draw(self):
        """Randomly acquired cards"""
        self.cur_index = (self.cur_index + 1) % self.__len__()
        if self.cur_index == 0:
            self.shuffle()
        return self.cards[self.cur_index]
