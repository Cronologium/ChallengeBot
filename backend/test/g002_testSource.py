from abstractTestSource import TestSource


class TestXandoSource(TestSource):
    def __init__(self):
        super(TestXandoSource, self).__init__()
        self.xs = ['0 0', '0 1', '0 2', '2 1', '2 2']
        self.os = ['1 0', '1 1', '1 2', '2 0']

        # =======
        # |X|X|O|
        # =======
        # |O|X|X|
        # =======
        # |X|O|O|
        # =======

    def game(self):
        play_with = self.socket.recv(1024)
        print 'I play with', play_with

        if play_with == 'X':
            for x in self.xs:
                print '===='
                print self.socket.recv(1024)
                self.socket.sendall(x)
        else:
            for o in self.os:
                print '===='
                print self.socket.recv(1024)
                self.socket.sendall(o)
        print '==='

if __name__ == '__main__':
    TestXandoSource().game()