from copy import deepcopy

import sys

class Api(object):
    def __init__(self):
        self.api = None

    def get_data(self):
        pass

    def feed(self, cmd):
        if 'exit' in cmd['meta']:
            sys.exit(0)