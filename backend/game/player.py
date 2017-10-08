from backend.game.status import Status


class Player(object):
    def __init__(self, name, timeout, id):
        self.name = name
        self.id = id
        self.timeout = timeout
        self.status = Status.PLAYS
        self.position = 50
        self.queue = []

    def store_data(self, data):
        self.queue.append(data)

    def get_data(self):
        data = (' '.join(self.queue) if len(self.queue) > 0 else '') + '\n'
        self.queue = []
        return data