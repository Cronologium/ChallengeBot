from api import Api

class BattleshipsApi(Api):
    def __init__(self):
        super(BattleshipsApi, self).__init__()
        self.api.my_board = [[' ' for x in xrange(10)] for y in xrange(10)]
        self.api.their_board = [[' ' for x in xrange(10)] for y in xrange(10)]

    def update_board(self, res, board):
        r = res.split(' ')
        board[int(r[1])][int(r[2])] = r[0]

    def feed(self, command):
        res = command.split('|')
        if res[0].startswith('miss'):
            self.update_board(res[0], self.api.their_board)
        elif res[0].startswith('hit'):
            self.update_board(res[0], self.api.their_board)
        elif res[0].startswith('put'):
            ints = [int(res[0].split(' ')[x]) for x in xrange(1, 5)]
            if ints[0] == ints[2]:
                for y in xrange(ints[0], ints[2] + 1):
                    self.api.my_board[ints[0]][y] = 'ship'
            elif ints[1] == ints[3]:
                for x in xrange(ints[1], ints[3] + 1):
                    self.api.my_board[x][ints[1]] = 'ship'

        if len(res) > 1:
            if res[1].startswith('miss'):
                self.update_board(res[1], self.api.my_board)
            elif res[1].startswith('hit'):
                self.update_board(res[1], self.api.my_board)

