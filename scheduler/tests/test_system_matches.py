# from .helper import ScheduleTestHelper
# from utils.tests.creations import certify_referee
# from ..models.match import MatchMeta as ModelMatch
# from utils.utils import get_timestamp
# from ..systems.match import (
#     TestMatch,
#     Match,
#     timedelta,
#     sleep
# )
#
#
# class MatchTestCase(ScheduleTestHelper):
#     def setup(self, referee=None, elite=False, future=timedelta()):
#         self.create_teams(1)
#         match_time = get_timestamp() + future
#         self.match = Match(
#             black=self.team_list[1],
#             white=self.team_list[0],
#             game_time=match_time,
#             logger=referee,
#             elite=elite
#         )
#
#     def setup_for_thread(self, referee=None, elite=False, future=timedelta()):
#         self.create_teams(1)
#         match_time = get_timestamp() + future
#         self.match = TestMatch(
#             black=self.team_list[1],
#             white=self.team_list[0],
#             game_time=match_time,
#             logger=referee,
#             elite=elite
#         )
#
#     def test_initializers_no_logger_not_elite(self):
#         print('initializers_no_logger_not_elite')
#         self.setup(future=timedelta(minutes=10))
#         match = ModelMatch.objects.filter(slug='a-vs-b')
#         self.assertTrue(match.exists())
#         self.assertFalse(match.first().is_logger)
#         self.assertEqual(self.match.minimum_game_length, timedelta(minutes=33))
#
#     def test_initializers_logger_elite(self):
#         print('initializers_logger_elite')
#         self.setup(future=timedelta(minutes=10), elite=True, referee=certify_referee(self.ref_data))
#         match = ModelMatch.objects.filter(slug='a-vs-b')
#         self.assertTrue(match.exists())
#         self.assertTrue(match.first().is_logger)
#         self.assertEqual(self.match.minimum_game_length, timedelta(minutes=43))
#
#     def test_start_no_referee(self):
#         print('start_no_referee')
#         self.setup(future=timedelta(minutes=-2))
#         with self.assertRaises(EnvironmentError):
#             self.match.start_game()
#
#     def test_start_to_early(self):
#         print('start_to_early')
#         self.setup(future=timedelta(minutes=5), referee=certify_referee(self.ref_data))
#         with self.assertRaises(EnvironmentError):
#             self.match.start_game()
#
#     def game_helper(self):
#         match_mdl = ModelMatch.objects.filter(slug='a-vs-b').first()
#         match_sys = self.match.get_match_object
#         self.assertEqual(match_mdl, match_sys)
#         return match_sys
#
#     def test_start_elite(self):
#         print('start_elite')
#         self.setup_for_thread(certify_referee(self.ref_data), True, timedelta(minutes=-2))
#         match_sys = self.game_helper()
#         self.match.start_game()
#         self.assertTrue(match_sys.did_game_start)
#         sleep(9)
#         self.assertTrue(match_sys.did_game_end)
#         self.assertEqual(len(match_sys.time_line), 6)
#
#     def test_add_goal(self):
#         self.setup_for_thread(certify_referee(self.ref_data), future=timedelta(minutes=-2))
#         match_sys = self.game_helper()
#         self.match.start_game()
#         self.assertTrue(match_sys.did_game_start)
#         sleep(2)
#         self.match.black_goal()
#         sleep(4)
#         self.match.white_goal()
#         from pprint import pprint
#         pprint(match_sys.time_line)
#
#     def test_add_goal_elite(self):
#         self.setup_for_thread(certify_referee(self.ref_data), True, timedelta(minutes=-2))
#         match_sys = self.game_helper()
#         self.match.start_game()
#         self.assertTrue(match_sys.did_game_start)
#         sleep(2)
#         self.match.black_goal()
#         sleep(4)
#         self.match.white_goal()
#         from pprint import pprint
#         pprint(match_sys.time_line)
