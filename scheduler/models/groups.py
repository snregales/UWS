from djongo import models

from teams.models import ParticipantStats, ParticipantStatsForm
from .matches import Match, MatchMeta


class GroupMetaManager(models.DjongoManager):
    def create_group(self, name, slug, teams=None):
        if teams:
            if not isinstance(teams, list):
                raise AttributeError('{} is not {}'.format(teams.__class__, list))
            for team in teams:
                if not isinstance(team, ParticipantStats):
                    raise AttributeError('{} is not {}'.format(team.__class__, ParticipantStats))

        group, create = Group.objects.get_or_create(
            name=name,
            slug=slug)
        meta = self.create(
            group=group,
            teams=teams if teams else [])
        return group, meta


class Group(models.Model):
    slug = models.SlugField(primary_key=True)
    name = models.CharField(max_length=1)
    concluded = models.BooleanField(default=False)
    objects = models.DjongoManager()

    class Meta:
        ordering = ['-concluded']

    def __str__(self):
        return self.name


class GroupMeta(models.Model):
    group = models.OneToOneField(Group, models.CASCADE)
    teams = models.ArrayModelField(
        model_container=ParticipantStats,
        model_form_class=ParticipantStatsForm,  # for manual input use only
    )
    matches = models.ArrayReferenceField(
        to=Match,
        on_delete=models.CASCADE,
        related_query_name='matches',
    )
    objects = GroupMetaManager()

    class Meta:
        ordering = ['group']

    def __str__(self):
        return self.group.name

    @property
    def is_group_concluded(self):
        return self.group.concluded

    @property
    def leaders(self):
        # return None if not self._leaders else self._leaders
        return

    @property
    def best_loser(self):
        # return self._best_loser
        return

    @property
    def _is_all_matches_done(self):
        """
         iterate through match list if match has no winner return False
         :return: False if any match is not done else True
         """
        for match in self.matches:
            if not match.did_game_end:
                return False
        return True

    def set_concluded(self):
        self.group.concluded = self._is_all_matches_done

    def set_leaders(self):
        """
        if group is concluded append the winner and runner up to _leader member variable
        """

    def set_best_loser(self):
        """
        if group is concluded add third position team in group to best loser
        """


    # TODO: validate participant coming in is unique
    def add_participants(self, teams):
        if not isinstance(teams, list):
            raise AttributeError('{} is not {}'.format(teams.__class__, list))
        for team in teams:
            if not (isinstance(team, ParticipantStats)):
                raise AttributeError('{} is not {}'.format(team.__class__, ParticipantStats))
        self.teams.extend(teams)
        return self.teams

    @staticmethod
    def _create_match_couples(teams):
        """
        create list tuples of <Team>'s, match, from a list of teams
        :param teams: list of <Team>'s
        :return: list of <Team> Tuples, [(<Team>, <Team>), (...), ...]
        """
        from itertools import combinations
        return list(combinations(teams, 2))

    def _team_list(self):
        """
        create a list of teams from the list of <Participant>'s; teams member variable
        :return: list of <Competitor>'s
        """
        from ..models.teams import Competitor
        return list(Competitor(team=team.team) for team in self.teams)

    def create_n_add_matches(self, event_name, times):
        """
        :param event_name: str object; name of the event
        :param times: list of <datetime.datetime>
        :return: list of <Match> references
        """
        couples = self._create_match_couples(self._team_list())
        if len(couples) != len(times):
            raise AttributeError('amount of times does not add up to the amount of couples')
        i = 0
        for (black, white), time in zip(couples, times):
            match, meta = MatchMeta.objects.create_match(black, white, time, event_name, self.__str__())
            self.matches.add(match)
            i += 1
        return self.matches