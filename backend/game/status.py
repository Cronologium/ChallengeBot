from backend.game.playbox.enums.abstractEnum import AbstractEnum


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
