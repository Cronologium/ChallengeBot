from copy import deepcopy


class ApiObject:
    def __init__(self):
        pass


class Api(object):
    def __init__(self):
        self.api = ApiObject()

    def get_data(self):
        return deepcopy(self.api)

    def feed(self, server_command):
        pass