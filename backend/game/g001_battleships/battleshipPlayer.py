from backend.game.playbox.abstract.coordinate import Coordinate
from backend.game.playbox.boards.battleshipsBoard import BattleshipsBoard
from backend.game.player import Player


class BattleshipPlayer(Player):
    def __init__(self, name, timeout):
        super(BattleshipPlayer, self).__init__(name, timeout)
        self.board = BattleshipsBoard()
        self.message_queue = []

    def put_ship(self, name, coords, size):
        start = Coordinate(coords[0], coords[1])
        finish = Coordinate(coords[2], coords[3])
        if self.board.can_put_ship(start, finish, size) is False:
            return None
        self.board.put_ship_coord(name, start, finish)
        return True

    def get_shot(self, coords):
        coord = Coordinate(coords[0], coords[1])
        if self.board.can_shoot(coords[0], coords[1]) is False:
            return None
        shooting_result = self.board.shoot(coords[0], coords[1])
        return shooting_result

    def has_no_ships(self):
        if self.board.get_ships_left() == 0:
            return True
        return False


