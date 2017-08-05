# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Game(models.Model):
    url = models.CharField(max_length=50)
    memory_limit = models.FloatField()
    time_limit = models.IntegerField()
    name = models.CharField(max_length=50)
    players_min = models.IntegerField(default=2)
    players_max = models.IntegerField(default=2)

    def __str__(self):
        return self.name


class Source(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, null=True)
    path = models.CharField(max_length=260)
    selected = models.BooleanField(default=0)
    LANGUAGE_CHOICES = (
        ('PY2', 'Python2'),
        ('Cpp', 'C++')
    )
    language = models.CharField(choices=LANGUAGE_CHOICES, default='PY2', max_length=20)
    RESULT_CHOICES = (
        ('P', 'Pending'),
        ('A', 'Accepted'),
        ('R', 'Rejected'),
        ('D', 'Disqualified'),
    )
    result = models.CharField(max_length=20, choices=RESULT_CHOICES, default='P')

    def get_selected_source(self, game):
        all_sources_set = Source.objects.filter(user=self, game=game)
        for i in range(all_sources_set.count()):
            if all_sources_set[i].selected:
                return all_sources_set[i]
        return None

    def __str__(self):
        return 'Source #' + str(self.id) + " U:" + self.user.username + " G:" + self.game.name


class Job(models.Model):
    STATUS_CHOICES = (
        ('R', 'Registered'),
        ('Q', 'Queued'),
        ('P', 'In progress'),
        ('F', 'Finished')
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Q')
    date = models.DateTimeField('Date of publication')
    game = models.ForeignKey(Game, on_delete=models.CASCADE, default=1)
    log_path = models.CharField(max_length=260, default='')
    author = models.ForeignKey(User, default=0)

    def __str__(self):
        return "Job #" + str(self.id) + " for " + self.game.name + " from " + str(self.date)


class Challenge(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, default=1)
    challengers = models.ManyToManyField(Source, through='Challenger')

    def __str__(self):
        return "ChallengeJob #" + str(self.job.id) + " for Game " + self.job.game.name


class Challenger(models.Model):
    STATUS_CHOICES = (
        ('W', 'Win'),
        ('T', 'Tie'),
        ('L', 'Lost'),
        ('D', 'Disqualified'),
        ('P', 'Pending')
    )
    challenge = models.ForeignKey(Challenge)
    source = models.ForeignKey(Source)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='P')
    position = models.IntegerField(default=0)

    def __str__(self):
        return self.challenge.job.game.name + ' ' + self.source.user.username + ' placed ' + str(self.position) + ' (' + self.status + ')'


class Submission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE, null=True)
    source = models.ForeignKey(Source, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return "Submission of " + self.user.username + " for " + \
               self.job.game.name + " from " + str(self.job.date)


class LevelGame(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    level = models.IntegerField()
    xp_reach = models.IntegerField()
    xp_win = models.IntegerField()
    xp_lost = models.IntegerField()
    xp_draw = models.IntegerField()
    xp_dsq = models.IntegerField()

    def __str__(self):
        return 'Level ' + str(self.level) + ' of game ' + self.game.name


class LevelingUser(models.Model):
    level = models.IntegerField()
    xp = models.IntegerField()
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username + ' (' + self.game.name + ' level ' + str(self.level) + ' | xp: ' + str(self.xp) + ')'