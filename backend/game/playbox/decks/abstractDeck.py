import random

from backend.game.playbox.exceptions.deckEmpty import DeckEmpty


class Deck(object):
    def __init__(self, cards=[]):
        self.cards = cards

    def __iter__(self):
        for card in self.cards:
            yield card
        raise StopIteration

    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self):
        if len(self.cards) == 0:
            raise DeckEmpty
        card = self.cards[0]
        if len(self.cards) > 1:
            self.cards = self.cards[1:]
        return card

    def put_cards(self, cards):
        for card in cards:
            self.cards.append(card)

    def empty(self):
        self.cards = []
