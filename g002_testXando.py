import sys

from backend.communication.server import Server
from backend.game.g002_xando.xandoGame import XandoGame
from backend.utils.consoleLogger import ConsoleLogger

if __name__ == '__main__':
    server = Server(int(sys.argv[1]))
    server.start()
    logger = ConsoleLogger()
    debug_logger = ConsoleLogger()
    game = XandoGame(debug_logger, logger, server, [('tester', 0.15), ('tester2', 0.15)])
    game.play()
    server.end()
