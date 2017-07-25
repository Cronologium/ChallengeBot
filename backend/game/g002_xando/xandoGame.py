from backend.game.abstractGame import Game
from backend.game.playbox.boards.xandoBoard import XandoBoard
from backend.game.player import Player
from backend.game.status import Status


class XandoGame(Game):
    def __init__(self, debug_logger, logger, server, players):
        super(XandoGame, self).__init__(debug_logger, logger, server,
                                        [Player(player[0], player[1]) for player in players],
                                        required_players=2,
                                        turns=9)
        self.player_turn = players[0][0]
        self.not_player_turn = players[1][0]
        self.marks_played = {'X': self.player_turn, 'O': self.not_player_turn}
        self.playing_marks = {v: k for k, v in self.marks_played.items()}
        self.board = XandoBoard()

    def start(self):
        super(XandoGame, self).start()
        self.server.send_message(self.player_turn, 'X')
        self.server.send_message(self.not_player_turn, 'O')
        for k, v in self.playing_marks.items():
            self.logger.log(k + ' plays ' + v)

    def turn(self):
        msg = self.server.send_and_receive(self.player_turn, self.board.stringify())
        try:
            if msg is None:
                raise Exception

            data = msg.split(' ')
            if len(data) != 2:
                raise Exception

            x, y = int(data[0]), int(data[1])
            if self.board.put_square(x, y, self.playing_marks[self.player_turn]) is False:
                raise Exception

        except Exception:
            self.players[self.player_turn].status = Status.INVALID_POSITION

        self.logger.log(self.board.stringify(sep=' | '))
        self.player_turn, self.not_player_turn = self.not_player_turn, self.player_turn

    def check(self):
        winner_sign = str(self.board.has_winner())
        if winner_sign != ' ':
            self.declare_winner(winner_sign)
        super(XandoGame, self).check()

    def end(self):
        for player_name in self.players:
            self.players[player_name].status = Status.DRAW
        super(XandoGame, self).end()

    def negative_sign(self, sign):
        if sign == 'X':
            return 'O'
        if sign == 'O':
            return 'X'

    def declare_winner(self, sign):
        print sign
        self.players[self.marks_played[sign]].status = Status.WINNER
        self.players[self.marks_played[self.negative_sign(sign)]].status = Status.LOSER
