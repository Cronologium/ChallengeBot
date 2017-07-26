from django.conf.urls import url
from django.views.generic import RedirectView

from . import views

app_name = 'web'
urlpatterns = [
    url(r'^aggressive_login$', views.aggressive_login, name='aggressive_login'),
    url(r'^games$', views.games, name='games'),
    url(r'^auth$', views.auth, name='auth'),
    url(r'^new_user$', views.new_user, name='new_user'),
    url(r'^logout$', views.log_out, name='log out'),
    url(r'^submit/(?P<game_id>[0-9]+)$', views.submit, name='submit'),
    url(r'^challenge_source/(?P<source_id>[0-9]+)$', views.challenge_source, name='challenge_source'),
    url(r'^game/(?P<game_id>[0-9]+)$', views.game, name='game'),
    url(r'^jobs$', RedirectView.as_view(url='/jobs/1/', permanent=False)),
    url(r'^jobs$(?P<job_page>[0-9]+)/', views.jobs, name='jobs'),
    url(r'^challenges$', views.challenges, name='challenges'),
    url(r'^support$', views.support, name='support'),
    url(r'^ticketsubmit$', views.ticket_submit, name='ticketsubmit'),
    url(r'^challenge/(?P<challenge_id>[0-9]+)$', views.challenge, name='challenge'),
    url(r'^about$', views.about, name='about'),
    url(r'^account/login$', views.auth_ajax, name='authenticate'),
    url(r'^', views.index, name='index'),

]

