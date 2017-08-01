# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

import re

# Create your views here.
from django.contrib.auth.models import User

from django.http import HttpResponse, Http404
from django.shortcuts import redirect, get_object_or_404
from django.template import loader
from django.utils import timezone

from .code_submit import submit_submission, submit_challenge
from .forms import SubmissionForm, ChallengeForm

from .models import Game, Challenge, Job, Submission, Source


def get_rendered_menu(request):
    context = {}
    if request.user.is_authenticated:
        context['username'] = request.user.username
    template = loader.get_template(os.path.join('web', 'menu.html'))
    return template.render(context, request)


def games(request):
    games_list = Game.objects.all()
    content_template = loader.get_template(os.path.join('web', 'games.html'))
    content_context = {'games_list': games_list}
    context = {}
    context['menu'] = get_rendered_menu(request)
    context['content'] = [content_template.render(content_context, request)]
    template = loader.get_template(os.path.join('web', 'template.html'))
    return HttpResponse(template.render(context, request))


def challenges(request):
    challenges_list = Challenge.objects.order_by('-id')
    content_template = loader.get_template(os.path.join('web', 'challenges.html'))
    content_context = {'challenges_list': challenges_list}
    context = {}
    context['menu'] = get_rendered_menu(request)
    context['content'] = [content_template.render(content_context, request)]
    template = loader.get_template(os.path.join('web', 'template.html'))
    return HttpResponse(template.render(context, request))


class Ship:
    def __init__(self, x1, y1, x2, y2, size, player):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.size = size
        self.player = player


class Shot:
    def __init__(self, x, y, player):
        self.x = x
        self.y = y
        self.player = player


def challenge(request, challenge_id):
    challenge_obj = get_object_or_404(Challenge, pk=int(challenge_id))
    content_template = loader.get_template(os.path.join('web', 'challenge.html'))
    log = None
    try:
        log = open(challenge_obj.log_path)
    except IOError:
        pass

    # What follows is bad code and *has* to changed
    participants = []
    ships = {}
    shots = {}
    line_index = 0
    for line in log:
        if line_index < 2:  # read participants' names
            participant = line.strip().split(' ')[1]
            participants.append(participant)
            ships[participant] = []
            shots[participant] = []
        else:
            line = line.strip().split(' ')
            if line[1] == 'puts':
                x1 = int(line[2])
                y1 = int(line[3])
                x2 = int(line[4])
                y2 = int(line[5])
                ship_size = abs(x1-x2) + abs(y1-y2) + 1
                player = line[0]
                ships[player].append(Ship(x1, y1, x2, y2, ship_size, player))
            if line[1] == 'shoots':
                x = int(line[2])
                y = int(line[3])
                player = line[0]
                shots[player].append(Shot(x, y, player))

        line_index += 1
    # Until here

    content_context = {'challenge': challenge_obj, 'participants': participants, 'ships': ships, 'shots': shots}
    context = {}
    context['menu'] = get_rendered_menu(request)
    context['content'] = [content_template.render(content_context, request)]
    template = loader.get_template(os.path.join('web', 'template.html'))
    return HttpResponse(template.render(context, request))


def game(request, game_id):
    game_obj = get_object_or_404(Game, pk=int(game_id))
    content_template = loader.get_template(os.path.join('web', 'game.html'))
    content_context = {'game': game_obj}
    if request.user.is_authenticated:
        content_context['form'] = SubmissionForm
    if Source.objects.filter(user_id=request.user.id, game_id=game_id, selected=1):
        content_context['p1_source'] = Source.objects.get(user_id=request.user.id, game_id=game_id, selected=1)
        content_context['opponents'] = ChallengeForm(game_id=game_id, user_id=request.user.id,
                                             max_players=game_obj.players_max - 1, min_players=game_obj.players_min - 1)
    template = loader.get_template(os.path.join('web', game_obj.url))
    content_context['game_description'] = template.render({}, request)
    context = {}
    context['menu'] = get_rendered_menu(request)
    context['content'] = [content_template.render(content_context, request)]
    template = loader.get_template(os.path.join('web', 'template.html'))
    return HttpResponse(template.render(context, request))


def jobs(request, job_page):
    job_page = int(job_page)
    job_list = Job.objects.order_by('-id')
    challenge_list = Challenge.objects.order_by('-id')
    submission_list = Submission.objects.order_by('-id')
    content_template = loader.get_template(os.path.join('web', 'jobs.html'))
    max_page = len(job_list) // 20 + 1
    if job_page > max_page:
        return redirect('/jobs/' + str(max_page) + '/')
    if len(job_list) > 20:
        min_job = max(len(job_list) - 20 * job_page, 0)
        max_job = min(len(job_list) - 20 * (job_page - 1), len(job_list))
        job_list = job_list[len(job_list) - max_job: len(job_list) - min_job]
    content_context = {
        'job_list': job_list,
        'challenge_list': challenge_list,
        'submission_list': submission_list,
        'max_page': max_page,
        'job_page': job_page,
    }
    context = {}
    context['menu'] = get_rendered_menu(request)
    context['content'] = [content_template.render(content_context, request)]
    template = loader.get_template(os.path.join('web', 'template.html'))
    return HttpResponse(template.render(context, request))


def about(request):
    content_template = loader.get_template(os.path.join('web', 'about.html'))
    content_context = {}
    context = {}
    context['menu'] = get_rendered_menu(request)
    context['content'] = [content_template.render(content_context, request)]
    template = loader.get_template(os.path.join('web', 'template.html'))
    return HttpResponse(template.render(context, request))


def index(request):
    content_template = loader.get_template(os.path.join('web', 'index.html'))
    content_context = {}
    context = {}
    context['menu'] = get_rendered_menu(request)
    context['content'] = [content_template.render(content_context, request)]
    template = loader.get_template(os.path.join('web', 'template.html'))
    return HttpResponse(template.render(context, request))

