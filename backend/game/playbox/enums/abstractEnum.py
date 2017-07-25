from enum import Enum


class AbstractEnum(Enum):
    def __str__(self):
        return self.value[0]