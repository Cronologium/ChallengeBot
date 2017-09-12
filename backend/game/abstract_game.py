import time

from backend.communication.channel import Channel
from backend.game.playbox.exceptions.game_over_exception import GameOver
from backend.game.status import Status


class Game(object):
    def __init__(self, debug_logger, screen, server, players, turns=99999999, required_players=2, accept_timeouts=False):
        self.screen = screen
        self.debug_logger = debug_logger
        self.server = server
        self.turns = turns
        self.required_players = required_players
        self.players = {}
        self.accept_timeouts = accept_timeouts
        self.win_pos = 1
        self.lose_pos = len(players)
        for player in players:
            self.players[player.name] = player

    def join_player(self, player_name, connection):
        self.players[player_name].joined = True
        self.server.bind_channel(player_name, Channel(connection, self.players[player_name].timeout))

    def kick_player(self, player_name):
        self.server.close_channel(player_name)
        self.players[player_name].joined = False

    def exit_player(self, player_name):
        self.queue_command(player_name, 'meta', 'exit')
        self.announce(player_name)
        self.server.close_channel(player_name)
        self.players[player_name].joined = False

    def interact(self, player_name):
        return self.server.send_and_receive(player_name, self.players[player_name].get_cmds())

    def announce(self, player_name):
        self.server.send_message(player_name, self.players[player_name].get_cmds())

    def queue_command(self, player_name, cmd_type, cmd):
        self.players[player_name].add_cmd(cmd_type, cmd)

    def players_win(self, names):
        for name in names:
            self.players[name].position = self.win_pos
            self.players[name].status = Status.WINNER
        self.win_pos += len(names)

    def players_lose(self, names):
        for name in names:
            self.players[name].position = self.lose_pos
            self.players[name].status = Status.LOSER
        self.lose_pos -= len(names)

    def players_dsq(self, dsq):
        for d in dsq:
            self.players[d[0]].position = len(self.players)
            self.players[d[0]].status = d[1]
        self.lose_pos -= len(dsq)
        for name in self.players:
            if self.players[name].status == Status.LOSER:
                self.players[name].position -= len(dsq)

    def start(self):
        while len([p for p in self.players if self.players[p].joined is False]):
            conn, player_name = self.server.get_blind_message()
            if player_name is not None and player_name in self.players and self.players[player_name].joined is False:
                self.join_player(player_name, conn)
            else:
                conn.close()
            time.sleep(0.2)

    def turn(self):
        raise NotImplementedError

    def end(self):
        self.screen.close()

    def early_game_over(self):
        pass

    def check(self):
        players_left = 0
        for player_name in self.players:
            if self.players[player_name].status != Status.PLAYS and self.players[player_name].joined:
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
                    self.players_win([player_name])
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
