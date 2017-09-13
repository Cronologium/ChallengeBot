from backend.game.screen import Screen


class XandoScreen(Screen):
    def __init__(self, logger, X_player, O_player):
        h = 3
        w = 3

        #MEDIA FILES
        self.black = "black.jpg"
        self.X = "X.png"
        self.O = "0.png"

        m = [[self.black for y in xrange(w)] for x in xrange(h)]
        super(XandoScreen, self).__init__(100, 100, w, h, logger, m, background=self.black, text=X_player + ': X<br>' + O_player + ': O')

    def put(self, x, y, mark):
        if mark == 'X':
            self.change_cells([(x, y, self.X)])
        elif mark == 'O':
            self.change_cells([(x, y, self.O)])
