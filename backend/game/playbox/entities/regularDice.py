from backend.game.playbox.entities.abstractDice import Dice


class RegularDice(Dice):
    def __init__(self):
        super(RegularDice, self).__init__([x for x in xrange(1, 7)])