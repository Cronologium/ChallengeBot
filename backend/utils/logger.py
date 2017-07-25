class Logger(object):
    def __init__(self):
        pass

    def open(self):
        raise NotImplementedError

    def close(self):
        raise NotImplementedError

    def log(self, message):
        raise NotImplementedError