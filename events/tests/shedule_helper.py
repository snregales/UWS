from datetime import timedelta
from django.contrib.auth import get_user_model
from django.test import TestCase
from utils.utils import get_timestamp
from teams.models import Team

User = get_user_model()


class EventTestHelper(TestCase):
    @classmethod
    def setUpClass(cls):
        print('-----'+cls.__name__+'-----')
        super().setUpClass()
        cls.email = 'example@gmail.com'
        cls.password = 'mypassword'
        cls.alias = 'kalonji'
        cls.admin_data = {
                'staff_alias': cls.alias,
                'admin_alias': cls.alias,
                'email': cls.email,
                'password': cls.password,
        }
        cls.name = 'Some Event Name'
        cls.date = get_timestamp().replace(second=0) + timedelta(days=200)
        cls.event_slug = 'some-event-name_' + str(cls.date.year)[2:]
        cls.model_meta = {
            'type': 'Underwater Rugby',
            'grade': 'Elite',
            'age_group': 0,
            'gender': 'Co-ed Teams',
        }
        cls.meta_form = cls.model_meta.copy()
        cls.meta_form.update({'age_group': 'Open'})
        cls.team_list = []

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


    def create_and_login(self, create):
        user = create(self.admin_data)
        self.client.login(**{'email': self.email, 'password': self.password})
        return user

    @classmethod
    def delete_event_instance(cls, slug):
        event = User.objects.filter(slug=slug)
        if event.exists():
            event.delete()

    @classmethod
    def delete_user_instance(cls, email):
        user = User.objects.filter(email__exact=email)
        if user.exists():
            user.delete()

    def tearDown(self):
        self.delete_user_instance(self.email)
        self.delete_event_instance(self.event_slug)
        self.delete_all_team_instances()

    @classmethod
    def tearDownClass(cls):
        print('')
        super().tearDownClass()
