from api import Api

from ctypes import *
class ApiObject(Structure):
    _fields_ = [("my_board", (c_char_p * 10) * 10),
                ("their_board", (c_char_p * 10) * 10),
                ("next_ship_size", c_int)]

    def __init__(self):
        super(ApiObject, self).__init__()
        for i in xrange(10):
            for j in xrange(10):
                self.my_board[i][j] = c_char_p('')
                self.their_board[i][j] = c_char_p('')

class BattleshipsApi(Api):
    def __init__(self):
        super(BattleshipsApi, self).__init__()
        self.api = ApiObject()

    def feed(self, cmd):
        super(BattleshipsApi, self).feed(cmd)
        for c in cmd['update']:
            r = c.split(' ')
            if r[0] == 'opponent':
                self.api.their_board[int(r[2])][int(r[3])] = c_char_p(r[1])
            elif r[0] == 'this':
                self.api.my_board[int(r[2])][int(r[3])] = c_char_p(r[1])
            elif r[0] == 'put':
                coords = [int(r[x]) for x in xrange(1, 5)]
                if coords[0] == coords[2]:
                    for y in xrange(coords[0], coords[2] + 1):
                        self.api.my_board[coords[0]][y] = c_char_p('ship')
                elif coords[1] == coords[3]:
                    for x in xrange(coords[1], coords[3] + 1):
                        self.api.my_board[x][coords[1]] = c_char_p('ship')

        for c in cmd['request']:
            r = c.split(' ')
            if r[0] == 'put':
                self.api.next_ship_size = int(r[1])

    def get_data(self):
        api = ApiObject()
        api.next_ship_size = int(self.api.next_ship_size)
        for i in xrange(10):
            for j in xrange(10):
                api.my_board[i][j] = c_char_p(str(self.api.my_board[i][j]))
                api.their_board[i][j] = c_char_p(str(self.api.their_board[i][j]))
        return api
