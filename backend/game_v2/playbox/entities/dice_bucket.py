class DiceBucket:
    def __init__(self, dices):
        self.dices = dices

    def get_values(self):
        return [dice.roll for dice in self.dices]

    def get_sum(self):
        return sum(self.get_values())
