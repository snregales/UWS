import itertools
from datetime import timedelta
from .helper import ScheduleTestHelper
from teams.models import ParticipantStats
from ..models.teams import Competitor
from ..models.groups import GroupMeta
from ..models.matches import MatchMeta
from utils.utils import get_timestamp

class GroupModelTestCases(ScheduleTestHelper):
    def setUp(self):
        self.group_name = 'A'
        self.group_slug = 'some-event' + '_' + self.group_name
        self.create_teams(3)
        self.participants, self.competitors = self.create_group_teams(self.team_list)
        self.group, self.meta = GroupMeta.objects.create_group(self.group_name, self.group_slug, self.participants)

    @staticmethod
    def create_match(teams, date, event, group=None):
        black, white = teams
        return MatchMeta.objects.create_match(
            black, white, date, event, group)

    @staticmethod
    def create_group_teams(teams):
        return list(ParticipantStats(team=team) for team in teams), list(Competitor(team=team) for team in teams)

    @staticmethod
    def tuples_bias(tuples, meta=False):
        return list(itertools.chain(*((itertools.compress(tuple, [not meta,meta]))
                                      for tuple in tuples)))

    @staticmethod
    def create_times(date, n):
        return list(date + timedelta(minutes=38*i) for i in range(n))

    def create_matches(self, dates):
        return list(self.create_match(couple, date, 'Some Event', 'A')
                    for couple, date in zip(self.create_match_couples(), dates))

    def create_match_couples(self):
        return list(itertools.combinations(self.competitors, 2))

    def test_create_group_wrong_input(self):
        print('create_group_wrong_input')
        with self.assertRaisesMessage(AttributeError, '{} is not {}'.format(self.competitors[1].__class__,
                                                                            ParticipantStats)):
            self.meta.add_participants(self.competitors)
        participant = ParticipantStats(team=self.team_list[0])
        with self.assertRaisesMessage(AttributeError, '{} is not {}'.format(participant.__class__, list)):
            self.meta.add_participants(participant)

    def test_add_participants(self):
        print('add_participants')
        self.assertEqual(len(self.meta.teams), 4)
        self.meta.add_participants(self.participants)
        self.assertEqual(len(self.meta.teams), 8)

    def test_add_participants_wrong_input(self):
        print('add_participants_wrong_input')
        with self.assertRaisesMessage(AttributeError, '{} is not {}'.format(self.competitors[1].__class__,
                                                                                   ParticipantStats)):
            GroupMeta.objects.create_group('B', 'my-group_B', self.competitors)
        competitor = Competitor(team=self.team_list[0])
        with self.assertRaisesMessage(AttributeError, '{} is not {}'.format(competitor.__class__, list)):
            GroupMeta.objects.create_group('B', 'my-group_B', competitor)

    def test_create_group(self):
        print('create group')
        self.assertEqual(self.group_slug, self.group.slug)
        self.assertEqual(len(self.meta.teams), 4)

    def match_times_assertion(self, queryset):
        time = None
        for qs in queryset:
            self.assertNotEqual(time, qs.scheduled)
            time = qs.scheduled

    def test_append_matches(self):
        print('append_matches')
        match_list = self.tuples_bias(self.create_matches(self.create_times(get_timestamp().replace(second=0), 6)))
        self.assertFalse(self.meta.matches.all())
        self.meta.matches.add(*match_list)
        self.assertEqual(len(self.meta.matches.all()), 6)
        self.match_times_assertion(self.meta.matches.all())


    def test_create_n_add_matches(self):
        print('create_n_add_matches')
        self.assertFalse(self.meta.matches.all())
        self.meta.create_n_add_matches('My Event', self.create_times(get_timestamp().replace(second=0), 6))
        self.assertEqual(len(self.meta.matches.all()), 6)
        self.match_times_assertion(self.meta.matches.all())
