import random


class Solution:
    def __init__(self):
        pass

    def put(self, api):
        x, y = random.randint(0, 2), random.randint(0, 2)
        while api.board[x][y] != '':
            x, y = random.randint(0, 2), random.randint(0, 2)
        return str(x) + " " + str(y)