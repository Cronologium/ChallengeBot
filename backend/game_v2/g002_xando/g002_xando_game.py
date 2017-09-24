import traceback

from backend.game_v2.abstract_game import Game
from backend.game_v2.g002_xando.g002_xando_screen import XandoScreen
from backend.game_v2.playbox.boards.g002_xando_board import XandoBoard
from backend.game_v2.player import Player
from backend.game_v2.status import Status


class XandoGame(Game):
    def __init__(self, debug_logger, logger, server, players):
        super(XandoGame, self).__init__(debug_logger,
                                        XandoScreen(logger, players[0][0], players[1][0]),
                                        server,
                                        [Player(player[0], player[1], player[2]) for player in players],
                                        required_players=2,
                                        turns=9)
        self.player_turn = players[0][0]
        self.not_player_turn = players[1][0]
        self.marks_played = {'X': self.player_turn, 'O': self.not_player_turn}
        self.playing_marks = {v: k for k, v in self.marks_played.items()}
        self.board = XandoBoard()

    def start(self):
        super(XandoGame, self).start()
        self.queue_command(self.playing_marks['X'], 'X')
        self.queue_command(self.playing_marks['O'], 'O')

    def turn(self):
        msg = self.interact(self.player_turn)
        try:
            if msg is None:
                raise Exception

            data = msg.split(' ')
            if len(data) != 2:
                raise Exception

            x, y = int(data[0]), int(data[1])
            if self.board.put_square(x, y, self.playing_marks[self.player_turn]) is False:
                raise Exception
            self.screen.put(x, y, self.playing_marks[self.player_turn])
            self.players[self.not_player_turn].add_cmd('update', str(x) + ' ' + str(y))

        except Exception:
            print traceback.format_exc()
            self.players_dsq([(self.player_turn, Status.INVALID_POSITION)])

        self.player_turn, self.not_player_turn = self.not_player_turn, self.player_turn

    def check(self):
        winner_sign = str(self.board.has_winner())
        if winner_sign != ' ':
            self.declare_winner(winner_sign)
        super(XandoGame, self).check()

    def end(self):
        self.players_win(self.players.keys())
        super(XandoGame, self).end()

    def negative_sign(self, sign):
        if sign == 'X':
            return 'O'
        if sign == 'O':
            return 'X'

    def declare_winner(self, sign):
        self.players_win([self.marks_played[sign]])
        self.players_lose([self.marks_played[self.negative_sign(sign)]])
