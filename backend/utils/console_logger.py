from backend.utils.logger import Logger


class ConsoleLogger(Logger):
    def __init__(self):
        super(ConsoleLogger, self).__init__()

    def open(self):
        pass

    def close(self):
        pass

    def log(self, message):
        print '[Log]', message