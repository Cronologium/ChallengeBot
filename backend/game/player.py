import json

from backend.game.status import Status


class Player(object):
    def __init__(self, name, timeout):
        self.joined = False
        self.name = name
        self.timeout = timeout
        self.status = Status.PLAYS
        self.position = 50
        self.cmds = {
            'request': [],
            'update': [],
            'meta': [],
        }

    def get_cmds(self):
        msg = json.dumps(self.cmds)
        self.cmds['request'] = []
        self.cmds['update'] = []
        self.cmds['meta'] = []
        return msg

    def add_cmd(self, cmd_type, cmd):
        self.cmds[cmd_type].append(cmd)