from django import forms
from djongo import models
# from athletes.models import Athlete


class TeamManager(models.DjongoManager):
    def create_team(self, **kwargs):
        from django.utils.text import slugify
        kwargs.update({
            'slug': slugify(kwargs['name'])
        })
        return self.create(**kwargs)


# TODO: use ArrayReferenceField to refer the athletes in a team
class Team (models.Model):
    slug = models.SlugField(primary_key=True)
    name = models.CharField(max_length=255, verbose_name='Team Name', unique=True)
    # athletes = models.ArrayReferenceField(
    #     to=Athlete,
    #     on_delete=models.CASCADE
    # )

    objects = TeamManager()

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class TeamUpdateForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ('name',)


class TeamCreateForm(TeamUpdateForm):
    def save(self, commit=True):
        return Team.objects.create_team(**self.cleaned_data)


class Stats(models.Model):
    goals = models.PositiveSmallIntegerField(verbose_name='Goals', default=0)
    wins = models.PositiveSmallIntegerField(verbose_name='Wins', default=0)
    loses = models.PositiveSmallIntegerField(verbose_name='Loses', default=0)
    draws = models.PositiveSmallIntegerField(verbose_name='Draws', default=0)

    class Meta:
        abstract = True


class TeamStats(Stats):
    team = models.OneToOneField(
        to=Team,
        on_delete=models.CASCADE
    )

    class Meta:
        ordering = ['loses', '-wins', '-draws', '-goals']

    def __str__(self):
        return self.team.name


class ParticipantStats(Stats):
    team = models.ForeignKey(
        to=Team,
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ['loses', '-wins', '-draws']
        abstract = True

    # following member function doesn't get called because class is abstract
    # TODO: figure out how to fix this problem
    def __str__(self):
        return self.team.name


class ParticipantStatsForm(forms.ModelForm):
    class Meta:
        model = ParticipantStats
        fields = ('team',)

    def __init__(self, *args, **kwargs):
        super(ParticipantStatsForm, self).__init__(*args, **kwargs)
        self.fields['team'] = forms.ModelChoiceField(
            Team.objects.all(),
            label='Teams in System',
            empty_label='Pick a Team'
        )
