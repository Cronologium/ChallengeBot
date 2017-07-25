from django import forms
from django.contrib.auth.models import User
from .models import Source
from .models import Ticket


class SubmissionForm(forms.Form):
    language = forms.ChoiceField(required=True, widget=forms.Select, choices=Source.LANGUAGE_CHOICES)


class ChallengeForm(forms.Form):
    def __init__(self, *args, **kwargs):
        game_id = kwargs.pop('game_id')
        user_id = kwargs.pop('user_id')
        self.min_players = kwargs.pop('min_players')
        self.max_players = kwargs.pop('max_players')
        all_sources = Source.objects.filter(game_id=game_id)
        self.CHOICES = []
        for source in all_sources:
            if source.user_id != user_id and source.selected != 0:
                self.CHOICES.append((source.id, User.objects.get(pk=source.user_id).username))

        super(ChallengeForm, self).__init__(*args, **kwargs)
        self.fields['eligible_opponents'].choices = self.CHOICES

    eligible_opponents = forms.MultipleChoiceField(required=True, widget=forms.SelectMultiple, choices=[])
    selected_opponents = forms.MultipleChoiceField(required=True, widget=forms.SelectMultiple, choices=[])


class TicketForm(forms.Form):
    title = forms.CharField(required=True, widget=forms.TextInput(attrs={'id': 'text-title',}), max_length=40)
    type = forms.ChoiceField(required=True, widget=forms.Select(attrs={'id': 'select-type',}), choices=Ticket.THEME_CHOICES)
    description = forms.CharField(required=True, widget=forms.Textarea(attrs={'id': 'text-description',}), max_length=1000)
