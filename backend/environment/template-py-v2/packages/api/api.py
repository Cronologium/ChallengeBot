from copy import deepcopy

import sys


class ApiObject:
    def __init__(self):
        pass


class Api(object):
    def __init__(self):
        self.api = ApiObject()

    def get_data(self):
        return deepcopy(self.api)

    def feed(self, cmd):
        if 'exit' in cmd['meta']:
            sys.exit(0)