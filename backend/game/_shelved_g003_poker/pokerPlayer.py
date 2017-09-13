from backend.game.player import Player


class PokerPlayer(Player):
    def __init__(self, name, timeout, money):
        super(PokerPlayer, self).__init__(name, timeout)
        self.money = money
        self.cards = [None, None]
        self.folded = True
        self.messages = []

    def deal_card(self, card):
        if self.cards[0] is None:
            self.cards[0] = card
        else:
            self.cards[1] = card
            self.folded = False

    def fold(self):
        self.folded = True
        cards = []
        cards.append(self.cards[0])
        cards.append(self.cards[1])
        self.cards = [None, None]
        return cards

    def bet(self, sum):
        if sum > self.money:
            sum = self.money
        self.money -= sum
        return sum

    def win(self, sum):
        self.money += sum

    def announce(self, message):
        self.messages.append(message)

    def get_messages(self):
        if len(self.messages) > 0:
            return ' | '.join(self.messages)
        else:
            return ''

    def get_cards(self):
        return str(self.cards[0]) + ' ' + str(self.cards[1])





