import random


class Solution:
    def __init__(self):
        self._smartShot = []
        self._enemyBoard = [['?' for _ in range(10)] for _ in range(10)]

        self._indexes = [0, 0, 0, 0, 0]
        self._sizes = {2: [], 3: [], 4: [], 5: []}
        self._generateShips()

    def _generateShips(self):

        self._sizes[5].append('0 0 0 4')
        self._sizes[4].append('1 0 1 3')
        self._sizes[3].append('3 0 3 2')
        self._sizes[3].append('4 0 4 2')
        self._sizes[2].append('6 0 6 1')

        '''
        self._sizes[4].append("ship 6 6 9 6")  # 0 0 0 0 0 0 0 0 0 0
        self._sizes[3].append("ship 8 0 8 2")  # 0 0 0 0 0 0 1 0 0 0
        self._sizes[3].append("ship 6 2 6 4")  # 0 1 0 0 0 1 0 0 0 0
        self._sizes[2].append("ship 4 8 4 9")  # 2 2 0 0 0 0 0 0 0 0
        self._sizes[2].append("ship 3 2 3 3")  # 0 0 0 0 2 0 0 0 2 2
        self._sizes[2].append("ship 4 4 5 4")  # 0 0 0 0 2 0 0 0 0 0
        self._sizes[1].append("ship 2 1 2 1")  # 0 0 3 3 3 1 4 0 0 0
        self._sizes[1].append("ship 1 6 1 6")  # 0 0 0 0 0 0 4 0 0 0
        self._sizes[1].append("ship 2 5 2 5")  # 3 3 3 0 0 0 4 0 0 0
        self._sizes[1].append("ship 6 5 6 5")  # 0 0 0 0 0 0 4 0 0 0
        '''

    def put_ship(self, server_command):
        """ Insert code here for ship placement """
        ba = bytearray()
        size = int(server_command.split(' ')[2])
        self._indexes[size] += 1
        ba.extend(map(ord, self._sizes[size][self._indexes[size] - 1]))
        return ba

    def shoot(self, server_command):
        """ Insert code here for shooting """
        x = y = -1
        res = server_command.split('|')[0].split(' ')

        if res[0] == "hit":
            self._enemyBoard[int(res[1])][int(res[2])] = 'x'
            self._addSmartShot(int(res[1]), int(res[2]))
        elif res[0] == "miss":
            self._enemyBoard[int(res[1])][int(res[2])] = 'o'

        x, y = self._shootSmart()

        ba = bytearray()
        ba.extend(map(ord, "shoot " + str(x) + " " + str(y)))
        return ba

    def _addSmartShot(self, x, y):
        if x > 0:
            self._smartShot.append([x - 1, y])
        if x < 9:
            self._smartShot.append([x + 1, y])
        if y > 0:
            self._smartShot.append([x, y - 1])
        if y < 9:
            self._smartShot.append([x, y + 1])

    def _shootSmart(self):
        while self._smartShot != []:
            x, y = self._smartShot.pop()
            if self._enemyBoard[x][y] == "?":
                return x, y
        return self._shootRandom()

    def _shootRandom(self):
        x = y = 0
        while self._enemyBoard[x][y] != "?":
            x = random.randint(0, 9)
            y = random.randint(0, 9)
        return x, y
