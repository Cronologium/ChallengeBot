from api import Api

class BattleshipsApi(Api):
    def __init__(self):
        super(BattleshipsApi, self).__init__()
        self.api.my_board = [['' for x in xrange(10)] for y in xrange(10)]
        self.api.their_board = [['' for x in xrange(10)] for y in xrange(10)]
        self.api.next_ship_size = 0

    def feed(self, cmd):
        super(BattleshipsApi, self).feed(cmd)
        for c in cmd['update']:
            r = c.split(' ')
            if r[0] == 'opponent':
                self.api.their_board[int(r[2])][int(r[3])] = r[1]
            elif r[0] == 'this':
                self.api.my_board[int(r[2])][int(r[3])] = r[1]
            elif r[0] == 'put':
                coords = [int(r[x]) for x in xrange(1, 5)]
                if coords[0] == coords[2]:
                    for y in xrange(coords[0], coords[2] + 1):
                        self.api.my_board[coords[0]][y] = 'ship'
                elif coords[1] == coords[3]:
                    for x in xrange(coords[1], coords[3] + 1):
                        self.api.my_board[x][coords[1]] = 'ship'

        for c in cmd['request']:
            r = c.split(' ')
            if r[0] == 'put':
                self.api.next_ship_size = int(r[1])





