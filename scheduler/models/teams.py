from djongo import models
from teams.models import Team
from django.forms import ModelForm


class Competitor(models.Model):
    team = models.ForeignKey(
        to=Team,
        on_delete=models.CASCADE,
    )
    color = models.CharField(
        max_length=5,
        choices=(('Black', 'black'),
                 ('White', 'white'),)
    )
    goals = models.PositiveSmallIntegerField(default=0)

    class Meta:
        abstract = True

    def __str__(self):
        return self.team.name + ' ' + self.color


class CompetitorForm(ModelForm):
    class Meta:
        model = Competitor
        exclude = ['goals']
