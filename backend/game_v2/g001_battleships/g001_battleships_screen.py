from backend.game_v2.screen import Screen


class BattleshipsScreen(Screen):
    def __init__(self, logger, first_player, second_player):
        h = 12
        w = 23
        self.players = {
            first_player: (1, 1),
            second_player: (1, 12)
        }

        # MEDIA FILES
        self.water = "water_block.jpg"
        self.ships = "ship*_**.png"
        self.hit = "hit.jpg"
        self.miss = "miss.jpg"
        self.black = "black.jpg"
        m = [[self.water for ww in xrange(w)] for hh in xrange(h)]
        cells = []
        for x in xrange(h):
            cells.append((x, 0, self.black))
            cells.append((x, w-1, self.black))
            cells.append((x, w//2, self.black))
        for y in xrange(1, w-1):
            cells.append((0, y, self.black))
            cells.append((h-1, y, self.black))
        super(BattleshipsScreen, self).__init__(25, 25, w, h, logger, m, background=self.water, cells=cells, text=first_player+': left<br>' + second_player+': right')

    def put_ship(self, player_name, coords):
        ship_template = self.ships[:4] + str(max(coords[3] - coords[1] + 1, coords[2] - coords[0] + 1)) + self.ships[5:7] + ("v" if coords[3] == coords[1] else "") + self.ships[8:]
        cells = []
        sc = self.players[player_name]
        if coords[3] == coords[1]:
            for x in xrange(coords[0], coords[2] + 1):
                cells.append((sc[0] + x, sc[1] + coords[1], ship_template[:6] + str(x - coords[0] + 1) + ship_template[7:]))
        else:
            for y in xrange(coords[1], coords[3] + 1):
                cells.append((sc[0] + coords[0], sc[1] + y, ship_template[:6] + str(y - coords[1] + 1) + ship_template[7:]))
        self.change_cells(cells)

    def shoot(self, player_name, coords, type):
        sc = self.players[player_name]
        if type == "hit":
            self.change_cells([(sc[0] + coords[0], sc[1] + coords[1], self.hit)])
        if type == "miss":
            self.change_cells([(sc[0] + coords[0], sc[1] + coords[1], self.miss)])



