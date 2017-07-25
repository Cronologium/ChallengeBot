import time

from backend.communication.channel import Channel
from backend.game.gameOver import GameOver
from backend.game.status import Status


class Game(object):
    def __init__(self, debug_logger, logger, server, players, turns=99999999, required_players=2, accept_timeouts=False):
        self.logger = logger
        self.debug_logger = debug_logger
        self.server = server
        self.turns = turns
        self.required_players = required_players
        self.players = {}
        self.accept_timeouts = accept_timeouts
        for player in players:
            self.players[player.name] = player

    def join_player(self, player_name, connection):
        print 'Player name', player_name
        self.players[player_name].joined = True
        self.server.bind_channel(player_name, Channel(connection, self.players[player_name].timeout))
        self.logger.log('Player ' + player_name + ' has joined the game!')

    def kick_player(self, player_name):
        self.server.close_channel(player_name)
        self.logger.log('Player ' + player_name + ' has been kicked from the game [' + str(self.players[player_name].status) + ']')
        self.players[player_name].joined = False

    def exit_player(self, player_name):
        self.server.exit_channel(player_name)
        self.logger.log('Player ' + player_name + ' has left the game! [' + str(self.players[player_name].status) + ']')
        self.players[player_name].joined = False

    def start(self):
        self.logger.open()
        while len([p for p in self.players if self.players[p].joined is False]):
            conn, player_name = self.server.get_blind_message()
            print player_name, 'tries to join'
            if player_name is not None and player_name in self.players and self.players[player_name].joined is False:
                self.join_player(player_name, conn)
            else:
                conn.close()
            time.sleep(0.2)

    def turn(self):
        raise NotImplementedError

    def end(self):
        self.logger.close()

    def early_game_over(self):
        pass

    def check(self):
        players_left = 0
        for player_name in self.players:
            if self.players[player_name].status != Status.PLAYS:
                if self.accept_timeouts and self.players[player_name].status == Status.TIMEOUT_EXCEEDED:
                    self.players[player_name].status = Status.PLAYS
                if self.players[player_name].status == Status.WINNER or \
                    self.players[player_name].status == Status.LOSER or \
                        self.players[player_name].status == Status.DRAW:
                    self.exit_player(player_name)
                else:
                    self.kick_player(player_name)
            else:
                players_left += 1

        if players_left < self.required_players:
            for player_name in self.players:
                if self.players[player_name].status == Status.PLAYS:
                    self.players[player_name].status = Status.WINNER
                    self.exit_player(player_name)
            raise GameOver

    def play(self):
        self.start()
        try:
            for turn_no in xrange(self.turns):
                self.turn()
                self.check()
        except GameOver:
            self.early_game_over()
        self.end()
