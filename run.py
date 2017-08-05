import sys

from backend.dispatcher import Dispatcher

if __name__ == '__main__':
    d = Dispatcher()
    d.reval()
    d.run()
