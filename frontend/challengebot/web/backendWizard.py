import os
import sqlite3
import socket
import random

from django.utils import timezone

from .models import User, Challenge, Submission, Game, Source, Job

HOST = 'localhost'
PORT = 1205

source_root = os.path.join(os.getcwd(), '..', '..', 'sources')
log_root = os.path.join(os.getcwd(), '..', '..', 'logs')


def save_source(data, extension, log=True):
    dictionary = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-'
    random_string = ''.join([dictionary[random.randint(0, len(dictionary) - 1)] for x in range(10)])
    root = source_root
    if log is True:
        root = log_root
    file_name = os.path.join(root, random_string)
    while os.path.exists(file_name):
        random_string = ''.join([dictionary[random.randint(0, len(dictionary) - 1)] for x in range(10)])
        file_name = os.path.join(root, random_string)
    file_name += extension
    fout = open(file_name, 'w')
    fout.write(data)
    fout.close()
    return file_name


def send_submission(game, user, data, language):
    extension = 'unk'
    if language == 'PY2' or language == 'PY3' or language == 'Python2' or language == 'Python3':
        extension = '.py'

    if language == 'Cpp' or language == 'C++':
        extension = '.cpp'

    source = Source()
    source.game = game
    source.user = user
    source.path = save_source(data, extension)
    source.save()

    job = Job()
    job.game = game
    job.status = 'R'
    job.date = timezone.now()
    job.save()

    sub = Submission()
    sub.source = source
    sub.user = user
    sub.job = job
    sub.save()

    #send_job("submission", [user.id], [source.id], game.id, job.id, sub.id)


def send_challenge(game, users, sources):
    job = Job()
    job.game = game
    job.status = 'R'
    job.date = timezone.now()
    job.save()

    challenge = Challenge()
    challenge.job = job
    challenge.log_path = save_source('', '.txt', log=True)
    challenge.save()
    for source in sources:
        challenge.challengers.add(source)
    challenge.save()

    #user_ids = [user.id for user in users]
    #source_ids = [source.id for source in sources]
    #send_job("challenge", user_ids, source_ids, game.id, job.id, challenge.id)
    return challenge
