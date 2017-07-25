class PlayingCard(object):
    def __init__(self, number, suit):
        self.number = number
        self.suit = suit

    def __str__(self):
        return str(self.number) + ' ' + str(self.suit)