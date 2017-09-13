from backend.game.playbox.decks.abstract_deck import Deck
from backend.game.playbox.entities.playing_card import PlayingCard
from backend.game.playbox.enums.card_suits import CardSuits


class PlayingCardsBasicDeck(Deck):
    def __init__(self):
        numbers = [str(x) for x in xrange(2, 10)] + ['J', 'Q', 'K', 'A']
        suits = [CardSuits.CLUBS, CardSuits.DIAMONDS, CardSuits.HEARTS, CardSuits.SPADES]
        cards = []
        for n in numbers:
            for s in suits:
                cards.append(PlayingCard(n, s))
        super(PlayingCardsBasicDeck, self).__init__(cards)