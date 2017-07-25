# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.

from .models import Game, Challenge, Source, Job, Submission, Ticket

admin.site.register(Game)
admin.site.register(Challenge)
admin.site.register(Source)
admin.site.register(Job)
admin.site.register(Submission)
admin.site.register(Ticket)
