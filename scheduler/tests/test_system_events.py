from ..systems.events import Scheduler
from .helper import ScheduleTestHelper
from utils.utils import get_timestamp
from teams.models import ParticipantStats
from datetime import datetime


class SchedulerTestCases(ScheduleTestHelper, Scheduler):
    def setup(self):
        self.event, self.meta = self.create_event('My Event', get_timestamp().replace(second=0))

    @staticmethod
    def create_event(name, date):
        data = {
            'type': 'Underwater Rugby',
            'grade': 'Elite',
            'age_group': 0,
            'gender': 'Co-ed Teams',
        }
        from events.models import EventMeta
        return EventMeta.objects.create_event(name, date, **data)

    def test_participant_list(self):
        print('participant_list')
        self.create_teams(4)
        p_list = self._participant_list(self.team_list)
        print(p_list)
        self.assertEqual(len(p_list), len(self.team_list))
        self.assertNotEqual(p_list, self.team_list)
        self.assertTrue(isinstance(p_list, list))
        for p in p_list:
            self.assertTrue(isinstance(p, ParticipantStats))
        del p_list

    def test_total_matches(self):
        print('total_matches')
        self.assertTrue(isinstance(self._total_matches([4,4]), int))
        self.assertEqual(self._total_matches([4,4,3]), 15)
        self.assertEqual(self._total_matches([3,3,3]), 9)

    def test_match_p_day(self):
        print('_match_p_day')
        matches = self._match_p_day(14)
        self.assertTrue(isinstance(matches, list))
        for match in matches:
            self.assertTrue(isinstance(match, int))
        self.assertEqual(matches, [7,7])
        self.assertEqual(self._match_p_day(12), [12])
        del matches


    def test_create_group_depths(self):
        print('create_group_depths')
        depths = self._create_group_depths(12,4)
        self.assertTrue(isinstance(depths, list))
        for depth in depths:
            self.assertTrue(isinstance(depth, int))
        self.assertEqual(depths, [4,4,4])
        self.assertEqual(self._create_group_depths(9,3), [3,3,3])
        del depths

    def test_group_combination(self):
        print('_group_combination')
        combo = self._group_combination(15)
        self.assertTrue(isinstance(combo, tuple))
        self.assertEqual(combo, (12,3))
        self.assertEqual(self._group_combination(14), (8,6))
        del combo

    def test__combined_depths(self):
        print('combined_depths')
        depths = self._combined_depths((12,3))
        self.assertTrue(isinstance(depths, list))
        for depth in depths:
            self.assertTrue(isinstance(depth, int))
        self.assertEqual(depths, [4,4,4,3])
        self.assertEqual(self._combined_depths((8,6)), [4,4,3,3])
        del depths

    def test_depth_per_group(self):
        print('depth_per_group')
        with self.assertRaises(EnvironmentError):
            self._depth_per_group(1)
        self.assertEqual(self._depth_per_group(7), [])
        self.assertEqual(self._depth_per_group(8), [4, 4])
        self.assertEqual(self._depth_per_group(9), [3, 3, 3])
        self.assertEqual(self._depth_per_group(10), [4, 3, 3])
        self.assertEqual(self._depth_per_group(11), [4, 4, 3])
        self.assertEqual(self._depth_per_group(12), [4, 4, 4])
        self.assertEqual(self._depth_per_group(13), [4, 3, 3, 3])
        self.assertEqual(self._depth_per_group(14), [4, 4, 3, 3])
        self.assertEqual(self._depth_per_group(15), [4, 4, 4, 3])
        self.assertEqual(self._depth_per_group(16), [4, 4, 4, 4])

    def test_create_times(self):
        print('create_times')
        times = self._create_times(3, datetime.strptime("21/11/18 8:00", "%d/%m/%y %H:%M"), 40)
        self.assertTrue(isinstance(times, list))
        for time in times:
            self.assertTrue(isinstance(time, datetime))
        del times

    def test_get_all_times(self):
        print('get_all_times')
        times = self._get_all_times(datetime.strptime("21/11/18 8:00", "%d/%m/%y %H:%M"), [7,7])
        self.assertTrue(isinstance(times, list))
        self.assertEqual(len(times), 14)
        for time in times:
            self.assertTrue(isinstance(time, datetime))
        del times

    def create_n_add_teams_to_event(self, teams):
        self.create_teams(teams)
        self.meta.add_team_to_event(self.team_list)
        self.assertEqual(len(self.meta.teams.all()), teams+1)

    def test_gather_components_for_event(self):
        print('gather_components_for_event')
        self.setup()
        self.create_n_add_teams_to_event(12)
        components = self._gather_components_for_event(self.event, self.meta.teams.all())
        self.assertTrue(isinstance(components, tuple))
        self.assertTrue(isinstance(components[0], list) and isinstance(components[1], list))
        self.assertEqual(len(components[0]), 4)
        self.assertEqual(len(components[1]), 4)
        for group in components[0]:
            self.assertTrue(isinstance(group, list))
            self.assertTrue(len(group) == 4 or len(group) == 3)
            for participants in group:
                self.assertTrue(isinstance(participants, ParticipantStats))
        for times in components[1]:
            self.assertTrue(isinstance(times, list))
            self.assertTrue(len(times) == 6 or len(times) == 3)
            for time in times:
                self.assertTrue(isinstance(time, datetime))
        self.event.delete()

    def test_event_manager(self):
        print('event_manager')
        self.setup()
        self.create_n_add_teams_to_event(12)
        meet = self._event_manager(self.event, self._gather_components_for_event(self.event, self.meta.teams.all()))
        self.assertEqual(meet.__str__(), 'My Event')
        self.assertEqual(len(meet.groups.all()), 4)



    @staticmethod
    def delete_event_instance(events):
        for event, meta in events:
            event.delete()

    @staticmethod
    def delete_group_instance(groups):
        for group, meta in groups:
            group.delete()
