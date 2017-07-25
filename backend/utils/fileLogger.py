from backend.utils.logger import Logger


class FileLogger(Logger):
    def __init__(self, file):
        super(FileLogger, self).__init__()
        self.file = file
        self.buffer = None

    def open(self):
        self.buffer = open(self.file, 'w')

    def close(self):
        self.buffer.close()
        self.buffer = None

    def log(self, message):
        self.buffer.write(message + '\n')