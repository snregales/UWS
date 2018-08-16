
from ..forms import RefereeRegistrationForm
from ..models import Referee
from utils.tests.helper import TestHelper


class RefereeForm(TestHelper):
    def test_valid_referee_form(self):
        print('valid_referee_form')
        data = {'email': 'another@gmail.com',
                'initial': self.password,
                'confirm': self.password,
                'first_name': self.first_name,
                'last_name': self.last_name}
        form = RefereeRegistrationForm(data=data)
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
            form = RefereeRegistrationForm(data=d)
            self.assertFalse(form.is_valid())

    def test_existing_user(self):
        print('invalid_referee_form')
        if 'dob' in self.data:
            del self.data['dob']
        Referee.objects.create_referee(**self.data)
        data = {'email': self.email,
                'initial': self.password,
                'confirm': self.password,
                'first_name': self.first_name,
                'last_name': self.last_name}
        form = RefereeRegistrationForm(data=data)
        self.assertFalse(form.is_valid())
