from datetime import timedelta
from djongo import models
from teams.models import Team
from utils.utils import get_utc_timestamp

grades = [
    ('Masters', 'Masters'),
    ('Elite', 'Elite'),
    ('Junior', 'Junior'),
    ('Beginner', 'Beginner'),
    ('Friendly', 'Friendly'),
]
age_groups = [
    (0, 'Open'),
    (19, 'U19'),
    (23, 'U23'),
]
types = [
    ('Hockey', 'Underwater Hockey'),
    ('Rugby', 'Underwater Rugby'),
]
genders = [
    ('Co-ed', 'Co-ed Teams'),
    ('Gendered', 'Gendered Teams'),
    ('Male', 'Male Only'),
    ('Female', 'Female Only'),
]


class EventQuerySet(models.QuerySet):
    from django.db.models import Q

    def get_event_instance_slug(self, slug):
        """
        search for an event that match slug
        :param slug: str obj
        :return: Event instance or None
        """
        event = self.filter(slug=slug)
        if event.exists():
            return event.first()
        return None

    def get_closed_events(self):
        """
        search for all closed registered Events that didn't happen yet
        :return: queryset
        """
        return self.filter(self.Q(closed=True) & self.Q(date__gt=get_utc_timestamp()) &
                           self.Q(date__lte=get_utc_timestamp() + timedelta(weeks=1)))

    def get_open_events(self):
        """
        search for all Events that their registration is still open
        :return: queryset
        """
        return self.filter(closed=False)

    # TODO: filter for events that already exceeded max amount of teams
    def get_events_that_need_to_close(self):
        return self.filter(self.Q(closed=False) &
                           self.Q(date__lte=get_utc_timestamp() + timedelta(weeks=1)))

class EventManager(models.DjongoManager):
    def get_queryset(self):
        return EventQuerySet(self.model, using=self._db)

    def close_events(self):
        """
        close all events that are a week from happening regardless if they are full or not
        :return: <QuerySet> events that just got closed
        """
        events = self.get_queryset().get_events_that_need_to_close()
        for event in events:
            event.closed = True
            event.save()
        return events


class Event (models.Model):
    """
    This uses embedded model field for meta, furthermore it also uses array reference
    field for the teams that are competing in the event
    """
    name = models.CharField(max_length=255, verbose_name='Name')
    slug = models.SlugField(unique=True)
    date = models.DateTimeField(verbose_name='Date')
    closed = models.BooleanField(default=False)
    objects = EventManager()

    class Meta:
        ordering = ['name']
        unique_together = ('name', 'date')

    def __str__(self):
        return self.name


class EventMetaManager(models.DjongoManager):
    def get_queryset(self):
        return EventQuerySet(self.model, using=self._db)

    def create_event(self, name, date, **kwargs):
        from django.utils.text import slugify
        event, create = Event.objects.get_or_create(
            name=name,
            date=date,
            slug=slugify(name + '_' + str(date.year)[-2:])
        )

        kwargs.update({'event': event})
        return event, self.create(**kwargs)


class EventMeta(models.Model):
    event = models.OneToOneField(Event, models.CASCADE)
    type = models.CharField(verbose_name='Event Type', max_length=6, choices=types, default='Hockey')
    grade = models.CharField(verbose_name='Competition Level', max_length=8, choices=grades, default='Friendly')
    age_group = models.PositiveSmallIntegerField(verbose_name='Age Group', choices=age_groups, default=0)
    gender = models.CharField(verbose_name='Gender Competing', max_length=8, choices=genders, default='Co-ed')
    teams = models.ArrayReferenceField(
        to=Team,
        on_delete=models.CASCADE,
        related_query_name='teams'
    )
    objects = EventMetaManager()

    def __str__(self):
        return self.event.name

    # TODO: Fix Problem
    # parent class failing to add a team to the back of the list, instead it replaces old data with new
    # weird thing it does it only on the server, tests all passes;
    # problem might not be here, but with the drop-down choice list given to the user on the template
    def add_team_to_event(self, team):
        from django.db.models.query import QuerySet
        if isinstance(team, list) or isinstance(team, QuerySet):
            for t in team:
                if not isinstance(t, Team):
                    raise ValueError('{} is not {}'.format(t.__class__, Team))
            self.teams.add(*team)
        else:
            if not isinstance(team, Team):
                raise ValueError('{} is not {}'.format(team.__class__, Team))
            self.teams.add(*[team])