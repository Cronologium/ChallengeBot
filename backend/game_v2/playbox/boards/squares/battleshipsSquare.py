from backend.game.playbox.boards.squares.abstractSquare import Square


class BattleshipsSquare(Square):
    FREE = 'free',
    SHIP = 'ship',
    HIT = 'hit',
    MISS = 'miss',
