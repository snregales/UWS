from django.forms import ModelForm
from django.db.models.signals import pre_save
from djongo import models

from ..utils import pre_save_receiver, init_log_referee
from .teams import Competitor, CompetitorForm
from .fouls import Foul
from referees.models import Referee
from teams.models import Team

ACTIONS = (
    ('Match Up', 'Match Up'),
    ('Start', 'Start'),
    ('Foul', 'Foul'),
    ('Goal', 'Goal'),
    ('Half Time Start', 'Half Time Start'),
    ('Half Time End', 'Half Time End'),
    ('Two Minute Warning', 'Two Minute Warning'),
    ('End', 'End'),
    ('Winner', 'Winner')
)


class TimeLine(models.Model):
    description = models.CharField(max_length=255, null=True)
    action = models.CharField(max_length=7, choices=ACTIONS)
    team = models.CharField(
        max_length=5,
        choices=(('Black', 'Black'), ('White', 'White')),
        null=True,
    )
    foul = models.ForeignKey(Foul, models.CASCADE, null=True)
    time = models.TimeField()
    timestamp = models.TimeField()

    class Meta:
        abstract = True

    # TODO: Refactor
    def __str__(self):
        if self.description:
            return self.action + ' | ' + self.description
        if self.action == 'Start' or self.action == 'End' or 'Half Time' in self.action or 'Warning' in self.action:
            return str(self.timestamp.replace(tzinfo=None)) + ' | ' + self.action
        line = str(self.timestamp.replace(tzinfo=None)) + ' | ' + str(self.time) + ' | ' + self.action
        if self.action == 'Foul':
            return line + ' | ' + self.team + ' | ' + str(self.foul)
        return line if not self.team else line + ' | ' + self.team


class TimeLineForm(ModelForm):
    models = TimeLine
    exclude = ('timestamp', 'description')


class Match(models.Model):
    slug = models.SlugField(primary_key=True)
    scheduled = models.DateTimeField()
    event = models.CharField(max_length=255, null=True, blank=True)
    group = models.CharField(max_length=2, null=True)
    playoff = models.BooleanField(default=False)
    winner = models.CharField(max_length=255, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = models.DjongoManager()

    class Meta:
        ordering = ['event', 'group', 'scheduled']
        unique_together = ['scheduled', 'event', 'group']

    def __str__(self):
        if self.playoff:
            return "{}: playoff match {}".format(self.event, self.matchmeta.__str__())
        return "{}, {}: match {}".format(self.event, self.group, self.matchmeta.__str__())

    @property
    def is_winner(self):
        return True if self.winner else False


pre_save.connect(receiver=pre_save_receiver, sender=Match)


class MatchMetaManager(models.DjongoManager):
    def create_match(self, black, white, scheduled, event, group=None, logger=None, *args, **kwargs):
        if not isinstance(black, Competitor):
            if not isinstance(black, Team):
                raise AttributeError('black is not Team nor Competitor')
            black = Competitor(team=black, color='Black')
        if not isinstance(white, Competitor):
            if not isinstance(white, Team):
                raise AttributeError('white is not Team nor Competitor')
            white = Competitor(team=white, color='White')
        playoff = False if group else True
        match, create = Match.objects.get_or_create(
            scheduled=scheduled,
            event=event,
            group=group,
            playoff=playoff
        )

        meta = self.create(
            match=match,
            referee=init_log_referee(logger),
            teams=[black, white],
            time_line=[
                TimeLine(description=(black.__str__() + ' - ' + white.__str__()), action='Match Up')
            ],
            *args, **kwargs)
        return match, meta


class MatchMeta(models.Model):
    match = models.OneToOneField(Match, models.CASCADE)
    started = models.DateTimeField(null=True)
    referee = models.ForeignKey(
        to=Referee,
        on_delete=models.CASCADE,
        null=True,
        limit_choices_to={
            'certified': True,
        }
    )
    teams = models.ArrayModelField(
        model_container=Competitor,
        model_form_class=CompetitorForm,  # for manual input purposes
    )
    time_line = models.ArrayModelField(
        model_container=TimeLine,
        model_form_class=TimeLineForm,  # for manual input purposes
    )
    final = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = MatchMetaManager()

    __half_time = False

    class Meta:
        ordering = ['match', '-started', 'final']
        indexes = [
            models.Index(name='last_modified', fields=['-updated', 'timestamp']),
        ]

    def __str__(self):
        return self.black_team_name + ' VS ' + self.white_team_name

    @property
    def black(self):
        return self.teams[0]

    @property
    def white(self):
        return self.teams[1]

    @property
    def black_team_name(self):
        return self.black.team.name

    @property
    def white_team_name(self):
        return self.white.team.name

    @property
    def logger_name(self):
        return self.referee.__str__ if self.referee else None

    @property
    def is_logger(self):
        return True if self.referee else False

    @property
    def did_game_start(self):
        return True if self.started else False

    @property
    def expected_start_time(self):
        return self.match.scheduled

    @property
    def game_started_at(self):
        return self.started if self.started else 'Game did not start'

    @property
    def did_game_end(self):
        return self.final

    @property
    def black_score(self):
        return self.black.color + ' ' + self.black_team_name + ' ' + str(self.black.goals)

    @property
    def white_score(self):
        return self.white.color + ' ' + self.white_team_name + ' ' + str(self.white.goals)

    def update_log_referee(self, logger):
        if logger and not logger.certified:
            raise AttributeError('logger is not certified')
        self.referee = logger

    def set_log_referee(self, logger):
        if self.is_logger:
            raise ValueError('referee already set')
        self.update_log_referee(logger)

    def start_match(self, timestamp):
        if not self.is_logger:
            raise EnvironmentError('No logging ref')
        if timestamp < self.match.scheduled:
            raise EnvironmentError('Tried to start game before scheduled time')
        self.started = timestamp
        self.time_line.append(TimeLine(
            action='Start',
            timestamp=timestamp
        ))

    def __did_game_start(self):
        if not self.did_game_start:
            raise EnvironmentError('Game did not start')

    def black_foul(self, foul, time, timestamp):
        self.__did_game_start()
        self.time_line.append(TimeLine(
            action='Foul',
            foul=foul,
            team='Black',
            time=time,
            timestamp=timestamp
        ))

    def white_foul(self, foul, time, timestamp):
        self.__did_game_start()
        self.time_line.append(TimeLine(
            action='Foul',
            foul=foul,
            team='White',
            time=time,
            timestamp=timestamp
        ))

    def record_two_minute_mark(self, timestamp):
        self.__did_game_start()
        self.time_line.append(TimeLine(
            action='Two Minute Warning',
            timestamp=timestamp
        ))

    def add_black_goal(self, time, timestamp):
        self.__did_game_start()
        self.black.goals += 1
        self.time_line.append(TimeLine(
            action='Goal',
            team='Black',
            time=time,
            timestamp=timestamp
        ))

    def add_white_goal(self, time, timestamp):
        self.__did_game_start()
        self.white.goals += 1
        self.time_line.append(TimeLine(
            action='Goal',
            team='White',
            time=time,
            timestamp=timestamp
        ))

    def record_start_half(self, timestamp):
        self.__did_game_start()
        self.__half_time = True
        self.time_line.append(TimeLine(
            action='Half Time Start',
            timestamp=timestamp
        ))

    def record_end_half(self, timestamp):
        self.__did_game_start()
        self.__half_time = False
        self.time_line.append(TimeLine(
            action='Half Time End',
            timestamp=timestamp
        ))

    def end_match(self, timestamp):
        self.final = True
        self.time_line.append(TimeLine(
            action='End',
            timestamp=timestamp
        ))

    def __get_match_winner(self):
        """
        compares black team's and white team's goals and either str or
        the team_dict with the most goals
        :return: 'Draw' or MatchTeam obj
        """
        if self.white.goals == self.black.goals:
            return 'Draw'
        return self.white_team_name if self.white.goals > self.black.goals else self.black_team_name

    def set_winner(self):
        """
        :raise EnvironmentError if game is not over
        set __winner to either str 'draw' or the team with the most goals
        """
        self.__did_game_start()
        self.match.winner = self.__get_match_winner()
        self.time_line.append(TimeLine(action='Winner', description=self.match.winner))
