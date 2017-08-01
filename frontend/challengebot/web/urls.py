from django.conf.urls import url
from django.views.generic import RedirectView

from .code_submit import submit_ajax, challenge_ajax
from .accounts import auth_ajax, reg_ajax, log_out
from . import views

app_name = 'web'
urlpatterns = [
    url(r'^games$', views.games, name='games'),
    url(r'^logout$', log_out, name='log out'),
    url(r'^game/(?P<game_id>[0-9]+)$', views.game, name='game'),
    url(r'^jobs$', RedirectView.as_view(url='/jobs/1', permanent=False)),
    url(r'^jobs/(?P<job_page>[0-9]+)$', views.jobs, name='jobs'),
    url(r'^challenges$', views.challenges, name='challenges'),
    url(r'^challenge/(?P<challenge_id>[0-9]+)$', views.challenge, name='challenge'),
    url(r'^about$', views.about, name='about'),
    # AJAX
    url(r'^account/login$', auth_ajax, name='authenticate'),
    url(r'^account/register$', reg_ajax, name='register'),
    url(r'^submit/source/(?P<game_id>[0-9]+)$', submit_ajax, name='submission'),
    url(r'^submit/challenge/(?P<source_id>[0-9]+)$', challenge_ajax, name='challenge_source'),
    url(r'^', views.index, name='index'),
]

