# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

import re
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

# Create your views here.
from django.contrib.auth.models import User

from django.http import HttpResponse, Http404
from django.shortcuts import redirect, get_object_or_404
from django.template import loader
from django.utils import timezone

from .forms import SubmissionForm, ChallengeForm, TicketForm

from . import backendWizard
from .models import Game, Challenge, Job, Submission, Source, Ticket

aggressive_auth = False


def get_rendered_menu(request):
    context = {}
    if request.user.is_authenticated:
        context['username'] = request.user.username
    template = loader.get_template(os.path.join('web', 'menu.html'))
    return template.render(context, request)


def games(request):
    if aggressive_auth is True and not request.user.is_authenticated:
        return redirect('/aggressive_login/')
    games_list = Game.objects.all()
    content_template = loader.get_template(os.path.join('web', 'games.html'))
    content_context = {'games_list': games_list}
    context = {}
    context['menu'] = get_rendered_menu(request)
    context['content'] = [content_template.render(content_context, request)]
    template = loader.get_template(os.path.join('web', 'template.html'))
    return HttpResponse(template.render(context, request))


def challenges(request):
    if aggressive_auth is True and not request.user.is_authenticated:
        return redirect('/aggressive_login/')
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
    if aggressive_auth is True and not request.user.is_authenticated:
        return redirect('/aggressive_login/')
    challenge_obj = None
    try:
        challenge_obj = Challenge.objects.get(pk=int(challenge_id))
    except Challenge.DoesNotExist:
        raise Http404('Challenge does not exist')
    content_template = loader.get_template(os.path.join('web', 'challenge.html'))
    log = None
    try:
        log = open(challenge_obj.log_path)
    except IOError:
        pass

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
            if line[1] == 'ship':
                x1 = int(line[2])
                y1 = int(line[3])
                x2 = int(line[4])
                y2 = int(line[5])
                ship_size = abs(x1-x2) + abs(y1-y2) + 1
                player = line[0][:-1]
                ships[player].append(Ship(x1, y1, x2, y2, ship_size, player))
            if line[1] == 'shoot':
                x = int(line[2])
                y = int(line[3])
                player = line[0][:-1]
                shots[player].append(Shot(x, y, player))

        line_index += 1

    content_context = {'challenge': challenge_obj, 'participants': participants, 'ships': ships, 'shots': shots}
    context = {}
    context['menu'] = get_rendered_menu(request)
    context['content'] = [content_template.render(content_context, request)]
    template = loader.get_template(os.path.join('web', 'template.html'))
    return HttpResponse(template.render(context, request))


def submit(request, game_id):
    if aggressive_auth is True and not request.user.is_authenticated:
        return redirect('/aggressive_login/')
    game_obj = None
    try:
        game_obj = Game.objects.get(pk=int(game_id))
    except Game.DoesNotExist:
        raise Http404("Game does not exist")
    form = SubmissionForm(request.POST)
    if request.POST['your_code'] == '':
        return redirect('/game/' + str(game_id) + '/')
    backendWizard.send_submission(game_obj, request.user, request.POST['your_code'], request.POST['language'])
    return redirect('/jobs/')


def challenge_source(request, source_id):
    if aggressive_auth is True and not request.user.is_authenticated:
        return redirect('/aggressive_login/')
    source_obj = get_object_or_404(Source, pk=int(source_id))
    game_obj = Game.objects.get(pk=source_obj.game_id)
    selected_opponents = request.POST.getlist('selected_opponents')
    users = [get_object_or_404(User, pk=source_obj.user_id)]
    sources = [source_obj]
    for opponent in selected_opponents:
        opponent_source = get_object_or_404(Source, pk=opponent)
        sources.append(opponent_source)
        user = get_object_or_404(User, pk=opponent_source.user_id)
        users.append(user)
    if game_obj.players_min <= len(users) <= game_obj.players_max:
        challenge = backendWizard.send_challenge(game_obj, users, sources)
        return redirect('/jobs/')
    return redirect('/game/' + str(game_obj.id) + '/')


def game(request, game_id):
    if aggressive_auth is True and not request.user.is_authenticated:
        return redirect('/aggressive_login/')
    game_obj = None
    try:
        game_obj = Game.objects.get(pk=int(game_id))
    except Game.DoesNotExist:
        raise Http404("Game does not exist")
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


def auth(request):
    if request.user.is_authenticated:
        logout(request)
    if 'username' in request.POST and 'password' in request.POST:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            login(request, user)
    return redirect('/')


def log_out(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('/')


def jobs(request, job_page):
    job_page = int(job_page)
    if aggressive_auth is True and not request.user.is_authenticated:
        return redirect('/aggressive_login/')
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


def support(request):
    if aggressive_auth is True and not request.user.is_authenticated:
        return redirect('/aggressive_login/')
    if request.user.is_authenticated:
        content_template = loader.get_template(os.path.join('web', 'support.html'))
        content_context = {'form': TicketForm(), 'ticket_list': Ticket.objects.filter(user=request.user)}
        context = {}
        context['menu'] = get_rendered_menu(request)
        context['content'] = [content_template.render(content_context, request)]
        template = loader.get_template(os.path.join('web', 'template.html'))
        return HttpResponse(template.render(context, request))
    else:
        return redirect('/')


def ticket_submit(request):
    if aggressive_auth is True and not request.user.is_authenticated:
        return redirect('/aggressive_login/')
    if request.user.is_authenticated:
        t = Ticket()
        t.date = timezone.now()
        t.type = request.POST['type']
        t.title = request.POST['title']
        t.user = request.user
        t.description = request.POST['description']
        t.save()
    return redirect('/support/')

def new_user(request):
    if 'username' in request.POST and 'password' in request.POST and 'email' in request.POST and 'confirm-password' in request.POST:
        username = request.POST['username']
        if re.search('^[a-zA-Z0-9]*$', username) is None:
            return redirect('/register/')
        email = request.POST['email']
        if re.search(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email) is None:
            return redirect('/register/')
        if len(User.objects.filter(username=username)) > 0:
            return redirect('/register/')
        if len(User.objects.filter(email=email)) > 0:
            return redirect('/register/')
        if request.POST['confirm-password'] != request.POST['password']:
            return redirect('/register/')
        user = User.objects.create_user(username, email, request.POST['password'])
        user.save()
    return redirect('/')

def aggressive_login(request):
    template = loader.get_template(os.path.join('web', 'aggressive_login.html'))
    return HttpResponse(template.render({}, request))


def about(request):
    if aggressive_auth is True and not request.user.is_authenticated:
        return redirect('/aggressive_login/')
    content_template = loader.get_template(os.path.join('web', 'about.html'))
    content_context = {}
    context = {}
    context['menu'] = get_rendered_menu(request)
    context['content'] = [content_template.render(content_context, request)]
    template = loader.get_template(os.path.join('web', 'template.html'))
    return HttpResponse(template.render(context, request))


def index(request):
    if aggressive_auth is True and not request.user.is_authenticated:
        return redirect('/aggressive_login/')
    content_template = loader.get_template(os.path.join('web', 'index.html'))
    content_context = {}
    context = {}
    context['menu'] = get_rendered_menu(request)
    context['content'] = [content_template.render(content_context, request)]
    template = loader.get_template(os.path.join('web', 'template.html'))
    return HttpResponse(template.render(context, request))

