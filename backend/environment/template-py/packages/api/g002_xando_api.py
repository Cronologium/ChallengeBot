from api import Api

class XandoApi(Api):
    def __init__(self):
        super(XandoApi, self).__init__()
        self.api.board = [[' ' for y in xrange(3)] for x in xrange(3)]
        self.api.playing = ' '

    def feed(self, cmd):
        super(XandoApi, self).feed(cmd)
        for c in cmd['update']:
            data = c.split(' ')
            self.api.board[int(data[0])][int(data[1])] = data[2]
        for c in cmd['request']:
            data = c.split(' ')
            if data[0] == 'play':
                self.api.playing = data[1]
