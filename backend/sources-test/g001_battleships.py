import random

class Solution:
    def __init__(self):
        self._sizes = {2: [], 3: [], 4: [], 5: []}
        self._sizes[5].append('0 0 0 4')
        self._sizes[4].append('1 0 1 3')
        self._sizes[3].append('3 0 3 2')
        self._sizes[3].append('4 0 4 2')
        self._sizes[2].append('6 0 6 1')
        pass

    def put(self, api):
        msg = self._sizes[api.next_ship_size][0]
        if len(self._sizes[api.next_ship_size]) > 1:
            self._sizes[api.next_ship_size] = self._sizes[api.next_ship_size][1:]
        return msg

    def shoot(self, api):
        x, y = random.randint(0, 9), random.randint(0, 9)
        while api.their_board[x][y] != '':
            x, y = random.randint(0, 9), random.randint(0, 9)
        return str(x) + " " + str(y)
