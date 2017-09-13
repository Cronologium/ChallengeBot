import random


class Dice(object):
    def __init__(self, values):
        self.values = values

    def roll(self):
        return random.choice(self.values)
