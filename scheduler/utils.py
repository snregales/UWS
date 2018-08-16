import itertools
from django.utils.text import slugify

def init_log_referee(logger):
    return logger if logger and logger.certified else None


def assert_slug_unique(model, slug):
    new_slug = slug
    if model.objects.filter(slug=slug).exists():
        it = 1
        while model.objects.filter(slug=new_slug).exists():
            new_slug = slug + '_' + str(it+1)
        return new_slug
    return slug


##########################################################################


def create_match_slug(instance):
    # slug should follow the following syntax <event>_<group>_<time>_\d
    mid = 'po' if instance.playoff else slugify(instance.group)
    slug = slugify(instance.event) + '_' + mid + '_' + slugify(instance.scheduled.time())
    return assert_slug_unique(instance.__class__, slug)


def pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_match_slug(instance)


################################################################################

class Slicer:
    def __init__(self):
        self.__teams = []
        self.__match_times = []
        self.__groups = None

    def set_slicer_var(self, teams, match_times, groups):
        """
        :param teams: list of <Participant>'s
        :param match_times: list of <datetime.datetime>'s
        :param groups: int
        :return:
        """
        self.__teams = teams
        self.__match_times = match_times
        self.__groups = groups

    def slicer_manager(self):
        """
        delegate task to workers
        :return: nested list of ordered <Participant>'s, nested list of ordered <datetime.datetime>'s
        """
        if self.__groups < 3 or self.__teams == 9 or not len(self.__teams) % 4:
            return self.__slicer(self.__teams, self.__match_times, self.__groups)
        if len(self.__teams) == 11 or len(self.__teams) == 14:
            return self._assistant(8, 12)
        return self._assistant(12, 18) if len(self.__teams) > 14 else self._assistant(6, 6) if len(self.__teams) < 13  else self._assistant(9, 9)

    def _assistant(self, team_mid, match_mid):
        groups = 3 if match_mid == 9 else 2
        if len(self.__teams) == 15: groups = 3
        head_teams, head_matches = self.__slicer(self.__teams[:team_mid], self.__match_times[:match_mid], groups)
        tail_teams, tail_matches = self.__slicer(self.__teams[team_mid:], self.__match_times[match_mid:],
                                                 groups if len(self.__teams) == 14 else None)
        return head_teams+tail_teams, head_matches+tail_matches

    def __slicer(self, teams, matches, chunks=None):
        return self.__cut(teams, chunks), self.__cut(matches, chunks)

    @staticmethod
    def __cut(lizt, chucks=None):
        return list(list(itertools.islice(lizt, group, None, chucks if chucks else 1))
                    for group in range(chucks if chucks else 1))


#####################################################################################################


class SchedulerStatics(Slicer):
    @staticmethod
    def _event_manager(event, group_config):
        """
        create or get <FixEvent instance, create all groups associated with it
        and populate group with all group configurations
        :param group_config: nested list of ordered tuples (<Team>,<datetime.datetime>)
        :return: <FixEvent> instance
        """
        from .models.groups import GroupMeta
        from .models.events import FixedEvent

        meet, m_meta = FixedEvent.objects.get_or_create(event=event)
        group_p, group_t = group_config
        groups = []
        for participants, times, i in zip(group_p, group_t, range(len(group_p))):
            name = str(chr(65+i))
            group, g_meta = GroupMeta.objects.create_group(name, event.slug + '_' + name, participants)
            g_meta.create_n_add_matches(event.name, times)
            groups.append(group)
        meet.add_to_group(groups)
        return meet

    @staticmethod
    def _participant_list(teams):
        """
        for team in event create a participant object of that team
        :param teams: list/queryset of Team objects, all __teams in event
        :return: list of <ParticipantStats>
        """
        from teams.models import ParticipantStats
        return list(ParticipantStats(team=team) for team in teams)

    @staticmethod
    def _total_matches(depth_p_group):
        """
        calculate the total amount of matches, matches per group = teams per group choose 2
        :param depth_p_group: list of depths; were each index represents a group and the value in it their depth
        :return: total number of matches
        """
        return sum(len(list(itertools.combinations(range(group), 2))) for group in depth_p_group)

    @staticmethod
    def _match_p_day(matches):
        """
        if matches is greater than what we can handle in a day split it in multiple days
        :param matches:
        :return:
        """
        # maximum days for group matches is 2, clients specs
        # might abstract it more to accept more days if client chooses to change his mind
        return [matches] if matches < 13 else [matches - matches // 2, matches // 2]

    @staticmethod
    def _create_group_depths(teams, depth):
        """
        calculate the amount groups, by dividing teams by depth
        method is only invoked if team mod 4 = 0 or team mod 3 = 0
        :param teams: int; total teams in event
        :param depth: int; max depth of a group in the event
        :return: list of ints; were each index represents a group and the value in it their depth
        """
        # TODO: variable check
        return list(depth for x in range(teams // depth))

    @staticmethod
    def _group_combination(teams):
        """
        calculate the amount of teams per group, this method is called
        when the amount of teams are not a modules of 4
        :param teams: ints; total teams in event
        :return: tuple <int, int>; (team//4, rest), where rest mod 3 = 0
        """
        i = 1
        while True:
            rest = teams - 4 * i
            if not rest % 3:
                return teams - rest, rest
            i += 1

    @staticmethod
    def _create_times(matches, date, minutes=38):
        """
        create, schedule, as many time stamps as they are matches for the date given
        timestamps are spaced by the minutes given
        :param matches: int; amount of matches to be scheduled
        :param date: <datetime.datetime>, date to be scheduled on
        :param minutes: int; minutes to spaced the matched by
        :return: list(<datetime.datetime>); list of all scheduled matches for that day
        """
        # might refactor timedelta as spacing parameter instead of int minutes
        from datetime import timedelta
        return list(date + (i * timedelta(minutes=minutes)) for i in range(matches))
