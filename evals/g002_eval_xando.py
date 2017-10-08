import sys


def read_int():
    return int(raw_input())

def read_string():
    return str(raw_input())

def main():
    board = [[' ' for x in xrange(3)] for y in xrange(3)]
    i_play = read_string()
    if i_play == 'X':
        for i in xrange(5):
            Y = 0
            X = 0
            for x in xrange(3):
                for y in xrange(3):
                    if board[x][y] == ' ':
                        X = x
                        Y = y
            board[X][Y] = 'X'
            print X, Y
            sys.stdout.flush()
            inp = read_string()
            x, y = inp.split(' ')
            x = int(x)
            y = int(y)
            board[x][y] = 'O'

    else:
        inp = ' '.join(i_play.split(' ')[1:])
        x, y = inp.split(' ')
        x = int(x)
        y = int(y)
        board[x][y] = 'X'
        for i in xrange(4):
            Y = 0
            X = 0
            for x in xrange(3):
                for y in xrange(3):
                    if board[x][y] == ' ':
                        X = x
                        Y = y

            board[X][Y] = 'O'
            print X, Y
            sys.stdout.flush()

            inp = read_string()
            x, y = inp.split(' ')
            x = int(x)
            y = int(y)
            board[x][y] = 'X'




if __name__ == '__main__':
    main()