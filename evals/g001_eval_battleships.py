import random
import sys

def read_int():
    return int(sys.stdin.readline())

def read_string():
    return str(sys.stdin.readline())


def main():
    sizes = {2: [], 3: [], 4: [], 5: []}
    sizes[5].append('0 0 0 4')
    sizes[4].append('1 0 1 3')
    sizes[3].append('3 0 3 2')
    sizes[3].append('4 0 4 2')
    sizes[2].append('6 0 6 1')

    board = [[False for x in xrange(10)] for y in xrange(10)]

    for x in xrange(5):
        size = read_int()
        ship = sizes[size][0]
        print ship
        sys.stdout.flush()
        if len(sizes[size]) > 1:
            sizes[size] = sizes[size][1:]

    for x in xrange(100):
        x, y = random.randint(0, 9), random.randint(0, 9)
        while board[x][y]:
            x, y = random.randint(0, 9), random.randint(0, 9)
        print x, y
        sys.stdout.flush()
        status = read_string()
        board[x][y] = True

if __name__ == '__main__':
    main()
