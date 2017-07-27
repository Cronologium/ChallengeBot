# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

import re
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

# Create your views here.
from django.contrib.auth.models import User

from django.http import HttpResponse, Http404, JsonResponse
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


def auth_ajax(request):
    if request.user.is_authenticated:
        logout(request)
    if 'username' in request.POST and 'password' in request.POST:
        if request.POST['username'] == '':
            return JsonResponse({'msg': 'Empty username.'})
        if request.POST['password'] == '':
            return JsonResponse({'msg': 'Empty password.'})
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            return JsonResponse({'msg': 'success'})
        else:
            return JsonResponse({'msg': 'Invalid username or password'})
    return JsonResponse({'msg': 'Missing username or password'})


def check_empty_fields(request):
    if 'username' not in request.POST:
        return {'reg-user-err': 'Please enter a username'}
    if 'email' not in request.POST:
        return {'reg-email-error': 'Please enter an e-mail address'}
    if 'password' not in request.POST:
        return {'reg-pass-error': 'Please enter a password'}
    if 'confirm-password' not in request.POST:
        return {'reg-confirm-error': 'Please confirm password'}
    return None


def validate_username(request):
    if request.POST['username'] == '':
        return {'reg-user-error': 'Please enter a username'}
    username = request.POST['username']
    if len(username) < 8:
        return {'reg-user-error': 'Username must contain at least 8 characters.'}
    if len(username) > 20:
        return {'reg-user-error': 'Username must contain at most 20 characters.'}
    if not re.match(r'^[A-Za-z].*', username):
        return {'reg-user-error': 'Username does not start with a letter'}
    if User.objects.filter(username=username).exists():
        return {'reg-user-error': 'Username is taken.'}
    if not re.match(r'^\w+$', username):
        return {'reg-user-error': 'Username can only contain letters, numbers and the underscore'}
    return None


def validate_email(request):
    if request.POST['email'] == '':
        return {'reg-email-error': 'Please enter an e-mail address.'}
    email = request.POST['email']
    if len(email) > 254:
        return {'reg-email-error': 'E-mail address is too long'}
    if User.objects.filter(email=email).exists():
        return {'reg-email-error': 'E-mail address already in use'}
    if re.search(r"[^@]+@[^@]+\.[a-zA-Z]+", email) is None:
        return {'reg-email-error': 'E-mail address looks invalid'}
    return None


def validate_password(request):
    if request.POST['password'] == '':
        return {'reg-pass-error': 'Please enter a password'}
    password = request.POST['password']
    if len(password) < 8:
        return {'reg-pass-error': 'Password too short.'}
    if len(password) > 35:
        return {'reg-pass-error': 'Password too long. How will you remember that?'}
    if not re.match(r'[A-Za-z0-9@#$%^&+=()!_*{}:;/".,?~`<>| \-\'\[\]\\]{8,35}', password):
        return {'reg-pass-error': 'Password contains invalid characters.'}
    if not re.search(r'[A-Za-z]+', password):
        return {'reg-pass-error': 'Password does not contain letters'}
    if not re.search(r'[0-9]+', password):
        return {'reg-pass-error': 'Password does not contain digits'}
    if not re.search(r'[^A-Za-z0-9]+', password):
        return {'reg-pass-error': 'Password does not contain symbols'}
    if password == request.POST['email']:
        return {'reg-pass-error': 'Password cannot match email address'}
    if password == request.POST['username']:
        return {'reg-pass-error': 'Password cannot match username'}
    return None


def validate_confirm_password(request):
    if request.POST['confirm-password'] == '':
        return {'reg-confirm-error': 'Please confirm password'}
    confirm_password = request.POST['confirm-password']
    if len(confirm_password) != len(request.POST['password']) or confirm_password != request.POST['password']:
        return {'reg-confirm-error': 'Passwords do not match!'}
    return None


def reg_ajax(request):
    err = False
    errors = {}
    empty_check = check_empty_fields(request)
    if empty_check is not None:
        return empty_check

    username_check = validate_username(request)
    if username_check is not None:
        err = True
        for key in username_check:
            errors[key] = username_check[key]

    email_check = validate_email(request)
    if email_check is not None:
        err = True
        for key in email_check:
            errors[key] = email_check[key]

    password_check = validate_password(request)
    if password_check is not None:
        err = True
        for key in password_check:
            errors[key] = password_check[key]

    confirm_check = validate_confirm_password(request)
    if confirm_check is not None:
        err = True
        for key in confirm_check:
            errors[key] = confirm_check[key]

    if not err:
        return JsonResponse({'': ''})
    else:
        return JsonResponse(errors)


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

