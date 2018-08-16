from django import forms

from .models import Event, EventMeta
from utils.utils import get_timestamp
from utils.validations import (
    validate_date,
    validate_event_name,
    validate_participants,
)


class EventForm(forms.ModelForm):
    current_year = get_timestamp().year
    name = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'placeholder': 'Aquamen Annual Underwater Mayhem'}))
    date = forms.DateTimeField(
        help_text='Date must be at least two weeks from now',
        widget=forms.SelectDateWidget(
            empty_label=('Year', 'Month', 'Day'),
            years=list(range(current_year, current_year + 10))))

    class Meta:
        model = EventMeta
        exclude = ('event', 'teams')

    field_order = ['name', 'date', 'type', 'grade', 'age_group', 'gender']

    def clean_date(self):
        return validate_date(self.cleaned_data.get('date'))

    def clean_name(self):
        return validate_event_name(self.cleaned_data.get('name'), Event)

    def save(self, commit=True):
        data = self.cleaned_data.copy()
        del data['name']
        del data['date']
        return EventMeta.objects.create_event(self.cleaned_data['name'], self.cleaned_data['date'], **data)


class AddTeamForm(forms.Form):
    def __init__(self, *args, **kwargs):
        from teams.models import Team
        if 'slug' not in kwargs:
            raise ValueError('slug is missing')
        self.slug = kwargs['slug']
        del kwargs['slug']
        super(AddTeamForm, self).__init__(*args, **kwargs)
        self.fields['teams'] = forms.ModelChoiceField(
            Team.objects.all(),
            label='Teams in System',
            empty_label='Pick a Team'
        )

    def clean_teams(self):
        return validate_participants(
            self.slug,
            self.cleaned_data.get('teams')
        )
