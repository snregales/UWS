from ..models.matches import Match as ModelMatch
from datetime import datetime, timedelta
from threading import Thread, Event
from time import sleep
from utils.utils import get_timestamp


class Match:
    _in_game_time = '00:00'
    _event = Event()

    def __init__(self, black, white, game_time, logger=None, elite=False):
        """
        use variables to create an Match model instance
        and initialize the rest of the class member variables
        :param black: Team obj
        :param white: Team obj
        :param game_time: datetime obj, match scheduled time
        :param logger: referee obj
        :param elite: bool obj, is this match elite level
        """
        from ..models.teams import Team
        from referees.models import Referee
        if not isinstance(game_time, datetime):
            raise ValueError('game_time is not a datetime obj')
        if not (isinstance(black, Team) and isinstance(white, Team)):
            raise ValueError('black and/or white is/are not a Team object(s)')
        if logger and not isinstance(logger, Referee):
            raise ValueError('logger is not Referee object')
        self._match = ModelMatch.objects.create_match(
            logger=logger,
            scheduled=game_time,
            black=black,
            white=white
        )
        self.__elite = elite
        self._match_half = self.__get_match_half
        self.__final = False

    @property
    def minimum_game_length(self):
        return 2 * self._match_half + timedelta(minutes=3)

    @property
    def get_in_game_time(self):
        return self._in_game_time

    @property
    def two_minute_mark(self):
        return timedelta(minutes=2)

    @property
    def end_game_allowed(self):
        return get_timestamp() > self._match.started + self.minimum_game_length if self._match.did_game_start else False

    @property
    def interrupt_allowed(self):
        return get_timestamp() > self._match.started + self.two_minute_mark if self._match.did_game_start else False

    @property
    def __start_game_allowed(self):
        return get_timestamp() > self._match.scheduled

    @property
    def _get_in_game_time(self):
        """
        converts _in_game_time str obj to a datetime.time obj
        :return: datetime obj
        """
        return datetime.strptime(self._in_game_time, '%M:%S').time()

    def interrupt_game(self, func=None):
        if not self.__elite:
            raise EnvironmentError('not an elite level game')
        if not self.interrupt_allowed:
            raise OSError('two minute mark not reached')
        if self._event.is_set():
            self._event.clear()
            func(self)
        else:
            self._event.set()

    def start_game(self):
        if not self.__start_game_allowed:
            raise EnvironmentError(
                'cannot start, game should start in ' + str(self._match.scheduled - get_timestamp())
            )
        if not self._match.is_logger:
            raise EnvironmentError('no assigned logger')
        secs = (2 * self._match_half).seconds

        def func(klass, sec):
            if sec == klass.two_minute_mark.seconds:
                klass._match.record_two_minute_mark(get_timestamp())

        self._event.set()
        args = (secs, func) if self.__elite else (secs,)
        Thread(target=self._countdown, args=args).start()

    def black_goal(self):
        def func(klass):
            klass._match.add_black_goal(klass._get_in_game_time, get_timestamp())
        try:
            self.interrupt_game(func)
            sleep(30)
            self.interrupt_game()
        except OSError or EnvironmentError:
            func(self)

    def white_goal(self):
        def func(klass):
            klass._match.add_white_goal(klass._get_in_game_time, get_timestamp())
        try:
            self.interrupt_game(func)
            sleep(30)
            self.interrupt_game()
        except OSError or EnvironmentError:
            func(self)

    def black_foul(self, foul):
        def func(klass):
            klass._match.black_foul(foul, klass._get_in_game_time, get_timestamp())
        try:
            self.interrupt_game(func)
        except EnvironmentError:
            func(self)

    def white_foul(self, foul):
        def func(klass):
            klass._match.white_foul(foul, klass._get_in_game_time, get_timestamp())
        try:
            self.interrupt_game(func)
        except EnvironmentError:
            func(self)

    def game_score(self):
        return self._match.black_score + ' ' + self._in_game_time + ' ' + self.__white_score

    # private
    @property
    def __white_score(self):
        return '' + str(self._match.white.goals) + ' ' + self._match.white_team_name + ' White'

    @property
    def __get_match_half(self):
        return timedelta(minutes=20) if self.__elite else timedelta(minutes=15)

    def __set__final(self):
        """
        :raise EnvironmentError if game is not over
        set Final to true
        """
        if not self.end_game_allowed():
            raise EnvironmentError('game still in session')
        self.__final = True
        self._match.end_match()
        self.__finalize_variables()

    def __finalize_variables(self):
        self._match.set_winner()
    #     self.__update_teams()
    #
    # def __update_teams(self):
    #     """
    #     :raise EnvironmentError if game not over
    #     update Team model in the database for the two teams in Match
    #     """
    #     if not self.__final:
    #         raise EnvironmentError('game not finished')
    #     self.__update_team_stat(self._match.black)
    #     self.__update_team_stat(self._match.white)
    #
    # def __update_team_stat(self, team):
    #     """
    #     appropriately update the team
    #     :param team: MatchTeam object
    #     """
    #     if self._match.winner == 'draw':
    #         team.draws += 1
    #     elif self._match.winner == team.team.name:
    #         team.wins += 1
    #     else:
    #         team.loses += 1

    def __half_time(self):
        self._match.record_start_half(get_timestamp())
        sleep(3 * 60)
        self._match.record_end_half(get_timestamp())
        self._match.save()

    def _countdown(self, secs, func=None):
        """
        is a background function that acts as an internal clock for the in-game time
        :param secs: int obj, total seconds of the game
        """
        self._match.start_match(get_timestamp())
        self._match.save()
        for i in range(secs, -1, -1):
            if i == self._match_half.seconds:
                self.__half_time()
            func(self, i)
            self._event.wait()
            minute, second = divmod(i, 60)
            self._in_game_time = '{:02d}:{:02d}'.format(minute, second)
            sleep(1)
        sleep(5)
        self._match.end_match(get_timestamp())


# NOTE: the following class is inheriting from Match and is for testing purposes only
class TestMatch(Match):
    def __init__(self, black, white, game_time, logger=None, elite=None):
        super(TestMatch, self).__init__(black, white, game_time, logger, elite)
        self._match_half = self.__get_match_half

    @property
    def get_match_object(self):
        return self._match

    @property
    def get_in_game_time(self):
        return self._in_game_time

    @property
    def two_minute_mark(self):
        return timedelta(seconds=2)

    @property
    def minimum_game_length(self):
        return (2*self._match_half) + timedelta(seconds=1)

    @property
    def _get_in_game_time(self):
        return datetime.strptime(self._in_game_time, '%M:%S').time()

    def _countdown(self, secs, func=None):
        self._match.start_match(get_timestamp())
        for i in range(secs, -1, -1):
            if i == self._match_half.seconds:
                self.__half_time()
            if func:
                func(self, i)
            self._event.wait()
            minute, second = divmod(i, 60)
            self._in_game_time = '{:02d}:{:02d}'.format(minute, second)
            sleep(1)
        self._match.end_match(get_timestamp())

    def __half_time(self):
        match = self.get_match_object
        match.record_start_half(get_timestamp())
        sleep(1)
        match.record_end_half(get_timestamp())

    def set_logger(self, logger):
        match = self.get_match_object
        match.set_log_referee(logger)
        match.save()

    @property
    def __get_match_half(self):
        return timedelta(seconds=3)
