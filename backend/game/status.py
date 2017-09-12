from backend.game.playbox.enums.abstract_enum import AbstractEnum


class Status(AbstractEnum):
    PLAYS = 'Plays',
    WINNER = 'Winner',
    LOSER = 'Loser',
    DRAW = 'Draw',
    TIMEOUT_EXCEEDED = 'Timeout exceeded',
    # Battleships
    INVALID_PUT = 'Invalid positioning',
    INVALID_SHOOT = 'Invalid shooting',
    # Xando
    INVALID_POSITION = 'Invalid position',
