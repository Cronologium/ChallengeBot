import sys

from backend.dispatcher_v2 import Dispatcher

if __name__ == '__main__':
    d = None
    if len(sys.argv) > 1:
        d = Dispatcher(start_port=int(sys.argv[1]))
    else:
        d = Dispatcher()
    d.clear()
    d.run()
