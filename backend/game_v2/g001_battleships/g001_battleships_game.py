import traceback

from backend.game_v2.g001_battleships.g001_battleships_player import BattleshipPlayer
from backend.game_v2.g001_battleships.g001_battleships_screen import BattleshipsScreen
from backend.game_v2.phasing_game import PhasingGame
from backend.game_v2.status import Status


class BattleshipGame(PhasingGame):
    def __init__(self, debug_logger, logger, players):
        self.ships_to_put = [
            ('destroyer', 2),
            ('submarine', 3),
            ('cruiser', 3),
            ('battleship', 4),
            ('carrier', 5)
        ]
        super(BattleshipGame, self).__init__(debug_logger,
                                             BattleshipsScreen(logger, players[0][0], players[1][0]),
                                             [BattleshipPlayer(player[0], player[1], player[2]) for player in players],
                                             phases={1: self.put_ship_turn, 2: self.shoot_ships_turn},
                                             turns=220,
                                             required_players=2)

        self.phase2_turn = self.players.keys()[0]
        self.phase2_not_turn = self.players.keys()[1]

    def log_ship_putting(self, player_name, poz):
        self.screen.put_ship(player_name, poz)

    def log_ship_shooting(self, player_name, poz, result):
        self.screen.shoot(player_name, poz, result)

    def put_ship_turn(self):
        if len(self.ships_to_put):
            for player in self.players:
                self.queue_command(player, str(self.ships_to_put[0][1]))
                msg = self.interact(player)

                if msg is None:
                    self.players_dsq([(player, Status.TIMEOUT_EXCEEDED)])
                else:
                    try:
                        data = msg.split(' ')
                        if len(data) != 4:
                            raise Exception
                        data = [int(x) for x in data]
                        if self.players[player].put_ship(self.ships_to_put[0][0], data, self.ships_to_put[0][1]) is None:
                            raise Exception
                        self.log_ship_putting(player, data)

                    except Exception:
                        print traceback.format_exc()
                        self.players_dsq([(player, Status.INVALID_PUT)])

            if len(self.ships_to_put) > 1:
                self.ships_to_put = self.ships_to_put[1:]
            else:
                self.phase = 2

    def shoot_ships_turn(self):
        msg = self.interact(self.phase2_turn)
        if msg is None:
            self.players_dsq([(self.phase2_turn, Status.TIMEOUT_EXCEEDED)])
        else:
            try:
                data = msg.split(' ')

                if len(data) != 2:
                    raise Exception
                data = [int(x) for x in data]

                result = self.players[self.phase2_not_turn].get_shot(data)
                self.log_ship_shooting(self.phase2_not_turn, data, result)
                if result is None:
                    raise Exception
                self.queue_command(self.phase2_turn, str(result))

            except Exception:
                self.players_dsq([(self.phase2_turn, Status.INVALID_PUT)])

        self.phase2_turn, self.phase2_not_turn = self.phase2_not_turn, self.phase2_turn

    def check(self):
        for player_name in self.players:
            if self.players[player_name].has_no_ships():
                self.players_lose([player_name])
        super(BattleshipGame, self).check()



