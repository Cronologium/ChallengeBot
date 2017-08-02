from backend.game.status import Status


class Player(object):
    def __init__(self, name, timeout):
        self.joined = False
        self.name = name
        self.timeout = timeout
        self.status = Status.PLAYS
        self.position = 50
