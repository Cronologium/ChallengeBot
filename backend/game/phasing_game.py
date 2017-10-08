from backend.game.abstract_game import Game
from backend.game.playbox.exceptions.game_over_exception import GameOver


class PhasingGame(Game):
    def __init__(self, debug_logger, screen, players, environment_manager,turns=99999999, required_players=2, phases={}):
        super(PhasingGame, self).__init__(debug_logger, screen, players, environment_manager, turns, required_players)
        self.phase = 1
        self.phases = phases

    def turn(self):
        pass

    def play(self):
        self.start()
        try:
            for turn_no in xrange(self.turns):
                if self.phase not in self.phases:
                    raise NotImplementedError

                self.turn()
                self.phases[self.phase]()
                self.check()
        except GameOver:
            self.early_game_over()
        self.end()
