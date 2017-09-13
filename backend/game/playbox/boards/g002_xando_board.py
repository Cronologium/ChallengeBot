from backend.game.playbox.boards.abstract_board import Board
from backend.game.playbox.boards.squares.xandoSquare import XandoSquare


class XandoBoard(Board):
    def __init__(self):
        super(XandoBoard, self).__init__(3, 3)
        for x in xrange(3):
            for y in xrange(3):
                self.board[x][y] = XandoSquare.EMPTY

    def put_square(self, x, y, square):
        if square == 'X':
            square = XandoSquare.X
        if square == 'O':
            square = XandoSquare.O
        if x < 0 or y < 0 or x > 2 or y > 2:
            return False
        if self.board[x][y] != XandoSquare.EMPTY:
            return False
        self.board[x][y] = square
        return True

    def has_winner(self):
        for x in xrange(3):
            presumptive_winner = self.board[x][0]
            for y in xrange(3):
                if presumptive_winner != self.board[x][y]:
                    presumptive_winner = XandoSquare.EMPTY
            if presumptive_winner != XandoSquare.EMPTY:
                return str(presumptive_winner)

        for y in xrange(3):
            presumptive_winner = self.board[0][y]
            for x in xrange(3):
                if presumptive_winner != self.board[x][y]:
                    presumptive_winner = XandoSquare.EMPTY
            if presumptive_winner != XandoSquare.EMPTY:
                return str(presumptive_winner)

        presumptive_winner = self.board[0][0]
        for x in xrange(3):
            if presumptive_winner != self.board[x][x]:
                presumptive_winner = XandoSquare.EMPTY
        if presumptive_winner != XandoSquare.EMPTY:
            return str(presumptive_winner)

        presumptive_winner = self.board[2][0]
        for x in xrange(3):
            if presumptive_winner != self.board[x][2-x]:
                presumptive_winner = XandoSquare.EMPTY
        if presumptive_winner != XandoSquare.EMPTY:
            return str(presumptive_winner)
        return str(XandoSquare.EMPTY)

    def stringify(self, sep='\n'):
        return sep.join([''.join([str(self.board[x][y]) for y in xrange(3)]) for x in xrange(3)])
