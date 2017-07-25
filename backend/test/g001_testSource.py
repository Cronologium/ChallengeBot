import sys

from abstractTestSource import TestSource


class TestBattleshipSource(TestSource):
    def __init__(self):
        super(TestBattleshipSource, self).__init__()
        self.positions = [(0, 0, 0, 4), (1, 0, 1, 3), (2, 0, 2, 2), (3, 0, 3, 2), (4, 0, 4, 1)]

    def get_shoot_coords(self):
        for x in xrange(10):
            for y in xrange(10):
                yield x, y
        raise StopIteration

    def get_put_coords(self):
        for i in xrange(len(self.positions)-1, -1, -1):
            yield self.positions[i]
        raise StopIteration

    def game(self):
        for x, y, z, t in self.get_put_coords():
            self.socket.recv(1024)
            self.socket.sendall(' '.join([str(x), str(y), str(z), str(t)]))

        for x, y in self.get_shoot_coords():
            msg = self.socket.recv(1024)
            if msg == '$exit':
                sys.exit(0)
            self.socket.sendall(' '.join([str(x), str(y)]))

if __name__ == '__main__':
    TestBattleshipSource().game()

