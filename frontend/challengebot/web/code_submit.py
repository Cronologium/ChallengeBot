from time import timezone

from django.utils import timezone

from .models import Submission, Source, Job, Challenge
from .utils import save_source


def submit_challenge(game, sources):
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

    return challenge


def submit_submission(game, user, data, language):
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
