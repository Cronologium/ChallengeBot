import sys

from game.g001_battleships.battleshipGame import BattleshipGame
from communication.server import Server
from utils.consoleLogger import ConsoleLogger


if __name__ == '__main__':
    server = Server(int(sys.argv[1]))
    server.start()
    logger = ConsoleLogger()
    debug_logger = ConsoleLogger()
    battleshipGame = BattleshipGame(debug_logger, logger, server, [('tester', 0.15), ('tester2', 0.15)])
    battleshipGame.play()
    server.end()