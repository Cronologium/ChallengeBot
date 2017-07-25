from backend.game.playbox.abstract.coordinate import Coordinate
from backend.game.playbox.boards.abstractBoard import Board
from backend.game.playbox.boards.squares.battleshipsSquare import BattleshipsSquare
from backend.game.playbox.entities.ship import Ship


class BattleshipsBoard(Board):
    def __init__(self):
        super(BattleshipsBoard, self).__init__(10, 10)
        self.ships = {}
        for x in xrange(10):
            for y in xrange(10):
                self.board[x][y] = BattleshipsSquare.FREE

    def can_put_ship(self, start, finish, size):
        if start.x < 0 or start.y < 0 or finish.x < 0 or finish.y < 0:
            return False
        if start.x > 9 or start.y > 9 or finish.x > 9 or finish.y > 9:
            return False
        if start.x != finish.x and start.y != finish.y:
            return False
        if start.x == finish.x and finish.y - start.y + 1 != size:
            return False
        if start.y == finish.y and finish.x - start.x + 1 != size:
            return False
        for x, y in Ship(start, finish):
            if self.board[x][y] == BattleshipsSquare.SHIP:
                return False
        return True

    def put_ship_coord(self, name, start, finish):
        ship = Ship(start, finish)
        for x, y in ship:
            self.board[x][y] = BattleshipsSquare.SHIP
        self.ships[name] = ship

    def put_ship(self, name, ship):
        for x, y in ship:
            self.board[x][y] = BattleshipsSquare.SHIP
        self.ships[name] = ship

    def is_not_destroyed(self, name):
        for x, y in self.ships[name]:
            if self.board[x][y] == BattleshipsSquare.SHIP:
                return True
        return False

    def get_ships_left(self):
        ships_left = 0
        for name in self.ships:
            if self.is_not_destroyed(name):
                ships_left += 1
        return ships_left

    def can_shoot(self, x, y):
        if x < 0 or y < 0 or x > 9 or y > 9:
            return False
        if self.board[x][y] in [BattleshipsSquare.MISS, BattleshipsSquare.HIT]:
            return False
        return True

    def shoot(self, x, y):
        if self.board[x][y] == BattleshipsSquare.SHIP:
            self.board[x][y] = BattleshipsSquare.HIT
        if self.board[x][y] == BattleshipsSquare.FREE:
            self.board[x][y] = BattleshipsSquare.MISS
        coordinate = Coordinate(x, y)
        hit_ship = None
        for name in self.ships:
            if self.ships[name].is_hit(coordinate) and not self.is_not_destroyed(name):
                hit_ship = name
                break
        if hit_ship is not None:
            del self.ships[hit_ship]
        return str(self.board[x][y])