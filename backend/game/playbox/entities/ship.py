from backend.game.g001_battleships.exceptions.invalidState import InvalidStateException


class Ship:
    def __init__(self, start, finish):
        self.start = start
        self.finish = finish
        if start.x > finish.x or start.y > finish.y:
            self.start = finish
            self.finish = start
        if not (self.start.x == self.finish.x or self.start.y or self.finish.y):
            raise InvalidStateException

    def is_hit(self, candidate):
        if self.start.x == self.finish.x:
            if candidate.x == self.start.x and self.start.y <= candidate.y <= self.finish.y:
                return True
            else:
                return False
        elif self.start.y == self.finish.y:
            if candidate.y == self.start.y and self.start.x <= candidate.x <= self.finish.x:
                return True
            else:
                return False
        else:
            raise InvalidStateException

    def __iter__(self):
        if self.start.x == self.finish.x:
            for y in xrange(self.start.y, self.finish.y + 1):
                yield self.start.x, y
            raise StopIteration
        elif self.start.y == self.finish.y:
            for x in xrange(self.start.x, self.finish.x + 1):
                yield x, self.start.y
            raise StopIteration
        else:
            raise InvalidStateException
