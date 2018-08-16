from .helper import ScheduleTestHelper
from utils.tests.creations import certify_referee
from ..models.matches import MatchMeta, Foul
from utils.utils import get_timestamp
from datetime import timedelta

ref_data = {
    'user': {
        'first_name': 'Justin',
        'last_name': 'Therian',
        'email': 'another@gmail.com',
        'password': 'mypassword',
    },
    'first_name': 'Justin',
    'last_name': 'Therian',
}


def foul_setup():
    Foul.objects.create(code='HL', name='Holding')
    Foul.objects.create(code='OP', name='Out of Play')
    Foul.objects.create(code='PD', name='Push Down')
    Foul.objects.create(code='SB', name='Surfaced Ball')


# TODO: properly test time_line
class ModelMatchTestCase(ScheduleTestHelper):
    def setup(self, event, group=None, referee=None, future=timedelta()):
        self.create_teams(1)
        match_time = get_timestamp() + future
        self.match, self.meta = MatchMeta.objects.create_match(
            scheduled=match_time,
            event=event,
            group=group,
            black=self.team_list[1],
            white=self.team_list[0],
            logger=referee,
        )

    def start_game(self):
        self.setup('Some Event', 'A', certify_referee(self.ref_data), timedelta(minutes=-2))
        start_time = get_timestamp()
        self.meta.start_match(start_time)
        return start_time

    def test_instance_creation(self):
        print('instance_creation')
        self.setup('Initial')
        self.assertIn('initial_po_', self.match.slug)
        self.assertEqual(self.meta.__str__(), 'A VS B')
        self.assertFalse(self.match.winner)
        self.assertFalse(self.match.is_winner)
        self.assertFalse(self.meta.did_game_end)
        self.assertFalse(self.meta.did_game_start)
        self.assertEqual(self.meta.game_started_at, 'Game did not start')
        self.assertEqual(self.meta.black_score, 'Black A 0')
        self.assertEqual(self.meta.white_score, 'White B 0')

    def test_instance_creation_logger_initialized(self):
        print('instance_creation_logger_initialized')
        ref = certify_referee(self.ref_data)
        self.setup('Initial', referee=ref)
        self.assertEqual(
            self.meta.logger_name,
            self.first_name + ' ' + self.last_name
        )
        self.assertTrue(self.meta.is_logger)
        with self.assertRaises(ValueError):
            self.meta.set_log_referee(ref)

    def test_instance_creation_logger_not_certify(self):
        print('instance_creation_logger_not_certify')
        ref = certify_referee(self.ref_data)
        ref.certified = False
        self.setup('Initial', referee=ref)
        self.assertFalse(self.meta.is_logger)
        with self.assertRaises(AttributeError):
            self.meta.set_log_referee(ref)

    def test_add_logger_to_an_existing_match(self):
        print('add_logger_to_an_existing_match')
        self.setup('Initial')
        self.assertFalse(self.meta.is_logger)
        self.meta.set_log_referee(certify_referee(self.ref_data))
        self.assertTrue(self.meta.is_logger)

    def test_set_n_update_logger(self):
        print('set_n_update_logger')
        ref = certify_referee(self.ref_data)
        self.setup('Initial', referee=ref)
        with self.assertRaises(ValueError):
            self.meta.set_log_referee(ref)
        ref.certified = False
        with self.assertRaises(AttributeError):
            self.meta.update_log_referee(ref)
        self.assertEqual(self.meta.logger_name, 'Sharlon Regales')
        self.meta.update_log_referee(certify_referee(ref_data))
        self.assertEqual(self.meta.logger_name, 'Justin Therian')
        self.delete_user_instance('another@gmail.com')

    def test_foul_game_not_started(self):
        print('foul_game_not_started')
        self.setup('Initial')
        with self.assertRaises(EnvironmentError):
            self.meta.black_foul(None, None, None)
            self.meta.white_foul(None, None, None)

    def test_foul(self):
        print('foul')
        start_time = self.start_game()
        foul_setup()
        self.meta.black_foul(Foul.objects.first(), timedelta(minutes=4), start_time + timedelta(minutes=4))
        self.meta.white_foul(Foul.objects.last(), timedelta(minutes=9), start_time + timedelta(minutes=9))
        self.assertEqual(len(self.meta.time_line), 4)

    def test_add_goals_to_teams_game_not_started(self):
        print('add_goals_to_teams_game_not_started')
        self.setup('Initial')
        with self.assertRaises(EnvironmentError):
            self.meta.add_black_goal(None, None)
            self.meta.add_white_goal(None, None)

    def test_add_goals_to_teams(self):
        print('add_goals_to_teams')
        start_time = self.start_game()
        self.meta.add_white_goal(timedelta(minutes=14), start_time + timedelta(minutes=16))
        self.assertEqual(self.meta.white_score, 'White B 1')
        self.meta.add_black_goal(timedelta(minutes=10), start_time + timedelta(minutes=20))
        self.meta.add_black_goal(timedelta(minutes=3), start_time + timedelta(minutes=27))
        self.assertEqual(self.meta.black_score, 'Black A 2')
        self.assertEqual(len(self.meta.time_line), 5)

    def test_half_time_game_not_stated(self):
        print('half_time_game_not_stated')
        self.setup('Initial', referee=certify_referee(self.ref_data))
        with self.assertRaises(EnvironmentError):
            self.meta.record_start_half(None)
            self.meta.record_end_half(None)

    def test_half_time(self):
        print('half_time')
        start_time = self.start_game()
        self.meta.record_start_half(start_time + timedelta(minutes=15))
        self.meta.record_end_half(start_time + timedelta(minutes=3))
        self.assertEqual(len(self.meta.time_line), 4)

    def test_two_minute_mark_game_not_started(self):
        print('two_minute_mark_game_not_started')
        self.setup('Initial')
        with self.assertRaises(EnvironmentError):
            self.meta.record_two_minute_mark(timedelta)

    def test_two_minute_mark(self):
        print('two_minute_mark')
        start_time = self.start_game()
        self.meta.record_two_minute_mark(start_time + timedelta(minutes=28))
        self.assertEqual(len(self.meta.time_line), 3)

    def test_end_tied_game(self):
        print('end_tied_game')
        start_time = self.start_game()
        self.assertFalse(self.meta.did_game_end)
        self.meta.end_match(start_time + timedelta(minutes=30))
        self.assertTrue(self.meta.did_game_end)
        self.assertFalse(self.match.is_winner)
        self.meta.set_winner()
        self.assertEqual(self.match.winner, 'Draw')
        self.assertEqual(len(self.meta.time_line), 4)

    def test_end_winning_game(self):
        print('end_winning_game')
        start_time = self.start_game()
        self.meta.add_white_goal(timedelta(minutes=14), start_time + timedelta(minutes=16))
        self.meta.add_black_goal(timedelta(minutes=10), start_time + timedelta(minutes=20))
        self.meta.add_black_goal(timedelta(minutes=3), start_time + timedelta(minutes=27))
        self.assertFalse(self.meta.did_game_end)
        self.meta.end_match(start_time + timedelta(minutes=30))
        self.assertTrue(self.meta.did_game_end)
        self.assertFalse(self.match.is_winner)
        self.meta.set_winner()
        self.assertEqual(self.match.winner, 'A')
        self.assertEqual(len(self.meta.time_line), 7)
