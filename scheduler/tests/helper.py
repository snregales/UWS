from django.test import TestCase
from profiles.views import User
from teams.models import Team, TeamStats


class ScheduleTestHelper(TestCase):
    @classmethod
    def setUpClass(cls):
        print('-----'+cls.__name__+'-----')
        super().setUpClass()
        cls.email = 'example@gmail.com'
        cls.password = 'mypassword'
        cls.first_name = 'Sharlon'
        cls.last_name = 'Regales'
        cls.ref_data = {
            'user': {
                'first_name': cls.first_name,
                'last_name': cls.last_name,
                'email': cls.email,
                'password': cls.password,
            },
            'first_name': cls.first_name,
            'last_name': cls.last_name,
        }
        cls.team_list = []

    def create_match_teams(self, n):
        if n < 0:
            return self.team_list
        team = Team.objects.create_team(**{'name': str(chr(65+n))})
        self.team_list.append(TeamStats.objects.create(team=team))
        self.create_match_teams(n - 1)

    def create_teams(self, n):
        if n < 0:
            return self.team_list
        self.team_list.append(Team.objects.create_team(**{'name': str(chr(65+n))}))
        self.create_teams(n - 1)

    def delete_all_team_instances(self):
        for team in self.team_list:
            team.delete()
        self.team_list.clear()

    @classmethod
    def delete_team_instance(cls, slug):
        team = Team.objects.filter(slug=slug)
        if team.exists():
            team.delete()

    @classmethod
    def delete_user_instance(cls, email):
        user = User.objects.filter(email__exact=email)
        if user.exists():
            user.delete()

    def tearDown(self):
        self.delete_user_instance(self.email)
        self.delete_all_team_instances()

    @classmethod
    def tearDownClass(cls):
        print('')
