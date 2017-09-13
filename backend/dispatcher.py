import threading
import traceback
from Queue import Queue

import time

from backend.aftergame.experience_manager import ExperienceManager
from backend.communication.server import Server
from backend.game.g001_battleships.g001_battleships_game import BattleshipGame
from backend.game.g002_xando.g002_xando_game import XandoGame
from backend.game.status import Status
from backend.environment.environments.manager import EnvironmentManager
from backend.utils.console_logger import ConsoleLogger
from backend.utils.empty_logger import EmptyLogger
from backend.utils.file_logger import FileLogger
from backend.utils.repository import Repository


class Dispatcher:
    def __init__(self, servers=4, start_port=1200, logger=ConsoleLogger()):
        self.servers = [Server(start_port+s) for s in xrange(servers)]
        self.games = {
            1: BattleshipGame,
            2: XandoGame,
        }
        self.evals = {
            1: './sources/g001_eval_battleships.py',
            2: './sources/g002_eval_xando.py',
        }
        self.repository = Repository('db.sqlite3')
        self.q = Queue()
        self.env_manager = EnvironmentManager()
        self.ended = False
        self.logger = logger
        self.experienceManager = ExperienceManager(self.repository, logger)

    def end(self):
        w = 5
        while w > 0:
            all_ok = True
            active = []
            for server in self.servers:
                if server.in_use:
                    all_ok = False
                    active.append(server)
                else:
                    server.end()
            if all_ok:
                w = 0
            else:
                w -= 1
            self.servers = active
        if len(self.servers) > 0:
            for server in self.servers:
                server.end()

    def run_client(self, source, memory_limit, port, id):
        username = 'eval'
        if 'user_id' in source:
            username = self.repository.select('auth_user', ['username'], {'id': source['user_id']})[0]['username']

        #print source, memory_limit, port
        try:
            env_id = self.env_manager.make_environment(source['path'], port)
            self.env_manager.run(env_id, memory_limit, username, id)
            self.env_manager.delete_environment(env_id)
        except Exception:
            print traceback.format_exc()

    def run_game(self, game, sources, memory_limit, ids, id):
        #print game, sources, memory_limit, ids
        for source in sources:
            t = threading.Thread(target=self.run_client, args=(source, memory_limit, game.server.port, id))
            t.start()
        game.play()
        self.repository.update('web_job', {'status': 'F'}, {'id': ids['job']})
        if 'submission' in ids:
            source_id = self.repository.select('web_submission', ['source_id'], {'id': ids['submission']})[0]['source_id']
            player_id = self.repository.select('auth_user', ['id'], {'username': [player for player in game.players if player != 'eval'][0]})[0]['id']
            winners = len([player for player in game.players.values() if player.status == Status.WINNER])
            losers = len([player for player in game.players.values() if player.status == Status.LOSER])
            draws = len([player for player in game.players.values() if player.status == Status.DRAW])
            if winners + losers + draws != 2:
                self.repository.update('web_source', {'result': 'R'}, {'id': source_id})
            else:
                self.repository.update('web_source', {'selected': 0}, {'user_id': player_id, 'selected': 1})
                self.repository.update('web_source', {'result': 'A', 'selected': 1}, {'id': source_id})
                self.experienceManager.do_submission(ids['submission'])
        elif 'challenge' in ids:
            challengers = self.repository.select('web_challenger', ['id', 'source_id'], {'challenge_id': ids['challenge']})
            for challenger in challengers:
                s = None
                for source in sources:
                    if source['id'] == challenger['source_id']:
                        s = source
                username = self.repository.select('auth_user', ['username'], {'id': s['user_id']})[0]['username']
                user_data = {}
                user_data['position'] = game.players[username].position
                if game.players[username].status == Status.WINNER:
                    user_data['status'] = 'W'
                elif game.players[username].status == Status.LOSER:
                    user_data['status'] = 'L'
                elif game.players[username].status == Status.DRAW:
                    user_data['status'] = 'T'
                else:
                    user_data['status'] = 'D'
                self.repository.update('web_challenger', user_data, {'id': challenger['id']})
            self.experienceManager.do_challenge(ids['challenge'])

    def executer(self):
        while not self.ended:
            if self.q.qsize() > 0 and len([server for server in self.servers if server.in_use is False]) > 0:
                free_servers = [server for server in self.servers if server.in_use is False]
                for server in free_servers:
                    server.in_use = True
                    run_data = self.q.get()
                    self.repository.update('web_job', {'status': 'P'}, {'id': run_data['job']['id']})
                    logger = None
                    players = []
                    sources = []
                    game_data = self.repository.select('web_game', ['id', 'time_limit', 'memory_limit'], {'id': run_data['job']['game_id']})[0]
                    game_data['time_limit'] = game_data['time_limit'] / 1000.0
                    ids = {'job': run_data['job']['id']}
                    if 'submission' in run_data:
                        logger = FileLogger(run_data['job']['log_path'])
                        logger.open()
                        s = self.repository.select('web_source', ['id', 'user_id', 'path', 'language'], {'id': run_data['submission']['source_id']})[0]
                        players.append(self.repository.select('auth_user', ['username'], {'id': s['user_id']})[0]['username'])
                        players.append('eval')
                        sources.append(s)
                        sources.append({'path': self.evals[run_data['job']['game_id']]})
                        ids['submission'] = run_data['submission']['id']
                    elif 'challenge' in run_data:
                        logger = FileLogger(run_data['job']['log_path'])
                        logger.open()
                        for challenger in run_data['challengers']:
                            s = self.repository.select('web_source', ['id', 'user_id', 'path', 'language'], {'id': challenger['source_id']})[0]
                            players.append(
                                self.repository.select('auth_user', ['username'], {'id': s['user_id']})[0]['username'])
                            sources.append(s)
                        ids['challenge'] = run_data['challenge']['id']
                    game = self.games[run_data['job']['game_id']](EmptyLogger(), logger, server, [(player, game_data['time_limit']) for player in players])
                    t = threading.Thread(target=self.run_game, args=(game, sources, game_data['memory_limit'], ids, game_data['id'],))
                    t.start()
            time.sleep(1)
        self.logger.log('executor finished')

    def consumer(self):
        while not self.ended:
            pending_jobs = self.repository.select('web_job', ['id', 'game_id', 'log_path'], {'status': 'R'})
            for job in pending_jobs:
                self.repository.update('web_job', {'status': 'P'}, {'id': job['id']})
                challenge = self.repository.select('web_challenge', ['id'], {'job_id': job['id']})
                if len(challenge) == 1:
                    challenge = challenge[0]
                    challengers = self.repository.select('web_challenger', ['source_id'], {'challenge_id': challenge['id']})
                    self.q.put({'job': job, 'challenge': challenge, 'challengers': challengers})
                    continue
                submission = self.repository.select('web_submission', ['id', 'user_id', 'source_id'], {'job_id': job['id']})
                if len(submission) == 1:
                    self.q.put({'job': job, 'submission': submission[0]})
                    continue
            time.sleep(1)
        self.logger.log('consumer finished')

    def run(self):
        for server in self.servers:
            server.start()
        try:
            executer_thread = threading.Thread(target=self.executer)
            executer_thread.start()
            self.consumer()
        except KeyboardInterrupt:
            self.ended = True
        self.logger.log('ending run')
        self.end()
        self.logger.log('end')

    def reval(self):
        self.repository.update('web_job', {'status': 'R'})
