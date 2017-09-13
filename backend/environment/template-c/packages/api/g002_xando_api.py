from api import Api
from ctypes import *

class ApiObject(Structure):
    _fields_ = [("playing", c_char),
                ("board", (c_char * 3) * 3)]

    def __init__(self):
        super(ApiObject, self).__init__()
        self.playing = ' '
        for i in xrange(3):
            for j in xrange(3):
                self.board[i][j] = c_char(' '[0])

class XandoApi(Api):
    def __init__(self):
        super(XandoApi, self).__init__()
        self.api = ApiObject()

    def feed(self, cmd):
        super(XandoApi, self).feed(cmd)
        for c in cmd['update']:
            data = c.split(' ')
            self.api.board[int(data[0])][int(data[1])] = c_char(chr(ord(data[2][0])))
        for c in cmd['request']:
            data = c.split(' ')
            if data[0] == 'play':
                self.api.playing = c_char(chr(ord(data[1][0])))

    def get_data(self):
        api = ApiObject()
        api.playing = c_char(chr(ord(str(self.api.playing)[0])))
        for i in xrange(3):
            for j in xrange(3):
                api.board[i][j] = c_char(chr(ord(str(self.api.board[i][j])[0])))
        return api

