import sys

from backend.dispatcher import Dispatcher

if __name__ == '__main__':
    d = Dispatcher()
    d.clear()
    d.run()
