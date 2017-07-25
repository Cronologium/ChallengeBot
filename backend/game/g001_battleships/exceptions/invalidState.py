class InvalidStateException(Exception):
    def __init__(self, message):
        super(InvalidStateException, self).__init__(message)