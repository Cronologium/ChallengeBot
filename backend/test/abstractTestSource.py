import socket
import sys


class TestSource(object):
    def __init__(self):
        self.socket = socket.socket()
        self.socket.connect(('localhost', int(sys.argv[2])))
        self.socket.sendall(sys.argv[1])

    def game(self):
        raise NotImplementedError