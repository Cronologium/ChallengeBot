from backend.game.g001_battleships.battleshipPlayer import BattleshipPlayer
from backend.game.phasingGame import PhasingGame
from backend.game.status import Status


class BattleshipGame(PhasingGame):
    def __init__(self, debug_logger, logger, server, players):
        self.ships_to_put = [
            ('destroyer', 2),
            ('submarine', 3),
            ('cruiser', 3),
            ('battleship', 4),
            ('carrier', 5)
        ]

        super(BattleshipGame, self).__init__(debug_logger, logger, server, [BattleshipPlayer(player[0], player[1]) for player in players],
                                             phases={1: self.put_ship_turn, 2: self.shoot_ships_turn},
                                             turns=220,
                                             required_players=2)

        self.phase2_turn = self.players.keys()[0]
        self.phase2_not_turn = self.players.keys()[1]

    def log_ship_putting(self, player_name, poz):
        self.logger.log(player_name + ' puts ' + ' '.join([str(p) for p in poz]))

    def log_ship_shooting(self, player_name, poz, result):
        self.logger.log(player_name + ' shoots ' + ' '.join([str(p) for p in poz]) + ' | ' + str(result))

    def put_ship_turn(self):
        if len(self.ships_to_put):
            for player in self.players:
                msg = self.server.send_and_receive(player, 'ship size ' + str(self.ships_to_put[0][1]))

                if msg is None:
                    self.players[player].status = Status.TIMEOUT_EXCEEDED
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
                        self.players[player].status = Status.INVALID_PUT

            if len(self.ships_to_put) > 1:
                self.ships_to_put = self.ships_to_put[1:]
            else:
                self.phase = 2
                self.players[self.phase2_turn].message_queue.append('start')

    def shoot_ships_turn(self):
        msg = self.server.send_and_receive(self.phase2_turn, '|'.join(self.players[self.phase2_turn].message_queue))
        self.players[self.phase2_turn].message_queue = []
        if msg is None:
            self.players[self.phase2_turn].status = Status.TIMEOUT_EXCEEDED
        else:
            try:
                data = msg.split(' ')

                if len(data) != 2:
                    raise Exception
                data = [int(x) for x in data]

                result = self.players[self.phase2_not_turn].get_shot(data)
                self.log_ship_shooting(self.phase2_turn, data, result)
                if result is None:
                    raise Exception
                self.players[self.phase2_not_turn].message_queue.append('shoots ' + msg)
                self.players[self.phase2_turn].message_queue.append(str(result) + ' ' + msg)

            except Exception:
                self.players[self.phase2_not_turn].status = Status.INVALID_SHOOT

        self.phase2_turn, self.phase2_not_turn = self.phase2_not_turn, self.phase2_turn

    def check(self):
        for player_name in self.players:
            if self.players[player_name].has_no_ships():
                self.players[player_name].status = Status.LOSER
        super(BattleshipGame, self).check()



