from ..models import Athlete
from ..forms import AthleteRegisterForm
from utils.tests.helper import TestHelper


class AthleteForm(TestHelper):
    def setUp(self):
        self.profile = Athlete.objects.create_athlete(**self.data)

    def test_valid_athlete_form(self):
        print('valid_athlete_form')
        data = {'email': self.email2,
                'initial': self.password,
                'confirm': self.password,
                'dob': self.dob,
                'first_name': self.first_name,
                'last_name': self.last_name}
        form = AthleteRegisterForm(data=data)
        self.assertTrue(form.is_valid())
        form.save()

    def test_missing_fields(self):
        print('missing_fields')
        data = [{},
                {'email': self.email},
                {'initial': self.password},
                {'confirm': self.password},
                {'first_name': self.first_name},
                {'last_name': self.last_name}]
        for d in data:
            form = AthleteRegisterForm(data=d)
            self.assertFalse(form.is_valid())

    def test_invalid_athlete_form(self):
        print('invalid_athlete_form')
        data = {'email': self.email,
                'initial': self.password,
                'confirm': self.password,
                'first_name': self.first_name,
                'last_name': self.last_name}
        form = AthleteRegisterForm(data=data)
        self.assertFalse(form.is_valid())
