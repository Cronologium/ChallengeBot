class Board(object):
    def __init__(self, width=0, height=0):
        self.board = [[None for x in xrange(width)] for y in xrange(height)]