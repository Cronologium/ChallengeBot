from backend.utils.logger import Logger


class EmptyLogger(Logger):
    def open(self):
        pass

    def log(self, line):
        pass

    def close(self):
        pass