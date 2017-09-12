from time import timezone

import re
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone

from .models import Submission, Source, Job, Challenge, Game, Challenger
from .utils import save_source


def validate_missing_fields(request):
    if 'language' not in request.POST:
        return {'msg': 'Missing language'}
    if 'code' not in request.POST:
        return {'code': 'Missing code'}
    return None


def validate_code(data, language):
    extension = ''
    if language == 'PY': # or language == 'PY' or language == 'Python2' or language == 'Python3':
        extension = '.py'
    elif language == 'C': # or language == 'C':
        extension = '.c'
    else:
        return {'msg': 'Unrecognized language'}
    if data == '':
        return {'msg': 'Missing code'}
    if len(data) < 30:
        return {'msg': 'Cannot submit source with this less characters'}
    if len(data) > 536870912:
        return {'msg': 'Source size must not exceed 64MB'}
    if not re.match(r'^[\x20-\x7E\r\n\0\t]+$', language):
        return {'msg': 'Code contains restricted characters'}
    return {'extension': extension}


def validate_sources(request, sources, source_reference):
    s = []
    game = source_reference.game

    user = source_reference.user
    if user != request.user:
        return {'msg': 'Your source is invalid'}
    players = {user.username: True}
    if len(sources) + 1 < game.players_min:
        return {'msg': 'Not enough players'}
    if len(sources) + 1 > game.players_max:
        return {'msg': 'Too many players'}

    for opponent in sources:
        opponent_source = get_object_or_404(Source, pk=int(opponent))
        s.append(opponent_source)
        if opponent_source.selected is False:
            return {'msg': 'Cannot challenge that source'}
        if opponent_source.game != game:
            return {'msg': 'Cannot challenge that source'}
        if opponent_source.user.username in players:
            return {'msg': 'Same player found multiple times'}
        players[opponent_source.user.username] = True
    return {'sources': s}


def submit_challenge(game, user, sources):
    job = Job()
    job.game = game
    job.status = 'R'
    job.date = timezone.now()
    job.author = user
    job.log_path = save_source('', '.txt', log=True)
    job.save()

    challenge = Challenge()
    challenge.job = job
    challenge.save()
    for source in sources:
        challenger = Challenger()
        challenger.source = source
        challenger.challenge = challenge
        challenger.save()
    return challenge


def submit_submission(game, user, data, extension):

    source = Source()
    source.game = game
    source.user = user
    source.path = save_source(data, extension)
    source.save()

    job = Job()
    job.game = game
    job.status = 'R'
    job.date = timezone.now()
    job.author = user
    job.log_path = save_source('', '.txt', log=True)
    job.save()

    sub = Submission()
    sub.source = source
    sub.user = user
    sub.job = job
    sub.save()


def submit_ajax(request, game_id):
    game_obj = get_object_or_404(Game, pk=int(game_id))
    data = validate_missing_fields(request)
    if data is not None:
        return JsonResponse(data)

    data = validate_code(request.POST['code'], request.POST['language'])
    if 'msg' in data:
        return JsonResponse({'msg': data['msg']})
    submit_submission(game_obj, request.user, request.POST['code'], data['extension'])
    return JsonResponse({'msg': 'success'})


def challenge_ajax(request, source_id):
    source_obj = get_object_or_404(Source, pk=int(source_id))
    if 'selected_opponents[]' not in request.POST:
        return JsonResponse({'msg': 'Missing players'})
    sources = request.POST.getlist('selected_opponents[]')
    data = validate_sources(request, sources, source_obj)
    if 'sources' not in data:
        return JsonResponse(data)
    submit_challenge(source_obj.game, request.user, [source_obj] + data['sources'])
    return JsonResponse({'msg': 'success'})