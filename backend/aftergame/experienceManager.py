from backend.utils.consoleLogger import ConsoleLogger


class ExperienceManager:
    def __init__(self, repository, logger):
        self.repository = repository
        self.logger = logger

    def award_xp(self, level_user, xp):
        level_user['xp'] += xp
        if level_user['xp'] < 0:
            level_user['xp'] = 0
        else:
            level_game = self.repository.select('web_levelgame', ['xp_reach'], {'level': level_user['level'], 'game_id': level_user['game_id']})
            if len(level_game) > 0:
                if level_game[0]['xp_reach'] != -1 and level_user['xp'] > level_game[0]['xp_reach']:
                    level_user['level'] += 1
                    level_user['xp'] -= level_game[0]['xp_reach']
        del level_user['game_id']
        self.repository.update('web_levelinguser', level_user, {'id': level_user['id']})

    def initiate_player(self, source_obj, level_start):
        self.logger.log('initiated a player: ' + str(source_obj) + ' at level ' + str(level_start))
        self.repository.insert('web_levelinguser', {'level': level_start, 'xp': 0, 'user_id': source_obj['user_id'], 'game_id': source_obj['game_id']})

    def do_submission(self, submission_id):
        submission = self.repository.select('web_submission', ['user_id', 'source_id'], {'id': submission_id})
        if len(submission) > 0:
            submissions = self.repository.select('web_submission', ['count(*)'], {'user_id': submission[0]['user_id'], 'source_id': submission[0]['source_id']})[0]['count(*)']
            source_obj = self.repository.select('web_source', ['user_id', 'game_id', 'result'], {'id': submission_id})
            if self.repository.select('web_levelinguser', ['count(*)'], {'user_id': source_obj[0]['user_id'], 'game_id': source_obj[0]['game_id']})[0]['count(*)'] != 0:
                return
            if len(source_obj) > 0:
                if submissions == 1 and source_obj[0]['result'] == 'A':
                    self.initiate_player(source_obj[0], 2)
                elif source_obj[0]['result'] == 'A':
                    self.initiate_player(source_obj[0], 1)

    def do_challenge(self, challenge_id):
        challengers = self.repository.select('web_challenger', ['source_id', 'status', 'position'], {'challenge_id': challenge_id})
        sources = [self.repository.select('web_source', ['id', 'game_id', 'user_id'], {'id': challengers[x]['source_id']})[0] for x in xrange(len(challengers))]
        level_game = self.repository.select('web_levelgame', ['level', 'xp_win', 'xp_lost', 'xp_draw', 'xp_dsq'], {'game_id': sources[0]['game_id']})
        if len(level_game) > 0:
            level = {level_game[x]['level']: {k: v for k, v in level_game[x].items() if k != 'level'} for x in xrange(len(level_game))}
            job_id = self.repository.select('web_challenge', ['job_id'], {'id': challenge_id})[0]['job_id']
            author_id = self.repository.select('web_job', ['author_id'], {'id': job_id})

            ranking = {}
            for ch in challengers:
                position = (ch['position'], ch['status'])
                source_id = ch['source_id']
                user_id = 0
                for s in sources:
                    if s['id'] == source_id:
                        user_id = s['user_id']
                        break
                ranking[user_id] = position

            for p in ranking:
                level_user_id = self.repository.select('web_levelinguser', ['id'], {'game_id': sources[0]['game_id'], 'user_id':p})[0]['id']
                level_user = self.repository.select('web_levelinguser', ['id', 'level', 'xp', 'game_id'], {'id': level_user_id})[0]
                if ranking[p][1] == 'D':
                    if author_id == p:
                        self.award_xp(level_user_id, int(1.5 * level[level_user['level']]['xp_dsq']))
                    else:
                        self.award_xp(level_user_id, level[level_user['level']]['xp_dsq'])
                else:
                    k = 0
                    for p2 in ranking:
                        if ranking[p2][0] > ranking[p][0]:
                            k += 1
                    xp_gain = 1.0 * (k * level[level_user['level']]['xp_win'] + (len(ranking) - 1) * level[level_user['level']]['xp_lost']) / (len(ranking) - 1)
                    if author_id == p:
                        xp_gain *= 1.5
                    self.award_xp(level_user, int(xp_gain))





