from datetime import timedelta
from events.models import Event
from ..utils import SchedulerStatics


class Scheduler(SchedulerStatics):
    """
    scheduler should be run automatically once a day, preferably at night
    NOTE: I cap the amount of teams that can register to any event to 16,
    I did this, because I want to keep the max amount of days for a tournament to 3 days one weekend
    since 16 teams creates 4 __groups of 4 teams. Which implies 4 * (4 choose 2) = 24 games
    And 8 teams in the playoffs, which results to 7 games. Thus this means for elite events with 16 teams
    role over = 22 group_game_breaks * 5 min + 6 playoff_game_break * 10 min = 2h 50m ~ 3h
    will take a minimum time of 31 games * 43 min + role over = 22h 13m + 3h = 25h 13m ~ 25h
    And none elite games would be 31 games + 33 min + role over = 17h 3m + 3h = 20h 3m ~ 20h
    """
    def schedule_events(self):
        """
        close event that needs closing
        query all closed events that didn't happened yet
        for events that are not yet organized delegate them to be organized
        :return: queryset, all the events that got scheduled
        """
        queryset = Event.objects.close_events()
        for event in queryset:
            # if teams in a event is less than 8 than there's no need for groups
            # event advances straight to playoffs
            teams = event.eventmeta.teams.all()
            if len(teams) > 7:
                self._event_manager(event, self._gather_components_for_event(event, teams))
        return queryset

    def _gather_components_for_event(self, event, teams):
        depth_p_group = self._depth_per_group(len(teams))
        times = self._get_all_times(event.date.replace(second=0, microsecond=0),
                                    self._match_p_day(self._total_matches(depth_p_group)))
        self.set_slicer_var(self._participant_list(teams), times, len(depth_p_group))
        return self.slicer_manager()

    def _depth_per_group(self, teams):
        """
        calculate the max depth and amount of groups needed for a Event instance
        :return: list of ints; were each index represents a group and the value in it their depth
        """
        if teams < 2: raise EnvironmentError('Not enough teams for a match')
        if teams < 8: return []
        if teams == 9: return self._create_group_depths(teams, 3)
        return self._create_group_depths(teams, 4) if not teams % 4 else self._combined_depths(self._group_combination(teams))

    def _get_all_times(self, date, match_p_day):
        """
        iteratively create datetime object, with 38 min difference in them, for the date given
        if the length of matches_p_day is greater than 1, for the length of match_p_day
        add a day and continue creating more datetime object for that day
        :param date: <datetime.datetime>, date that the event starts or is scheduled for
        :param match_p_day: list(<int>); each index represents a day,
        and each value the amount of matches for that day
        :return: list(<datetime.datetime>); all the match times
        """
        times = []
        for matches, days in zip(match_p_day, range(len(match_p_day))):
            times += self._create_times(matches, date + timedelta(days=days))
        return times

    def _combined_depths(self, combination):
        """
        get list for of depths from each combination of mod 4 and mod 3,
        method is called when total teams, adding the values of combination, mod 4 is not 0
        :param combination: tuple of <int>'s; where firts mod 4 = 0 and second mod 3 = 0
        :return: list of ints; were each index represents a group and the value in it their depth
        """
        # TODO: variable check
        four, three = combination
        return self._create_group_depths(four, 4) + (self._create_group_depths(three, 3))
