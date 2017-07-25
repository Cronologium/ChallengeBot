from enum import Enum


class Square(Enum):
    def __str__(self):
        return self.value[0]