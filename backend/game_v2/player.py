from backend.game_v2.status import Status


class Player(object):
    def __init__(self, name, timeout, port):
        self.joined = False
        self.name = name
        self.port = port
        self.timeout = timeout
        self.status = Status.PLAYS
        self.position = 50
        self.queue = []

    def store_data(self, data):
        self.queue.append(data)

    def get_data(self):
        data = ' '.join(self.queue) if len(self.queue) > 0 else ''
        self.queue = []
        return data