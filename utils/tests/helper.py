from datetime import datetime
from copy import deepcopy
from django.contrib.auth import get_user_model
from django.test import TestCase

User = get_user_model()


class TestHelper(TestCase):
    @classmethod
    def setUpClass(cls):
        print('-----'+cls.__name__+'-----')
        super().setUpClass()
        cls.email = 'example@gmail.com'
        cls.email2 = 'another@gmail.com'
        cls.password = 'mypassword'
        cls.first_name = 'Sharlon'
        cls.last_name = 'Regales'
        cls.dob = datetime.date(datetime.strptime('1993-09-28', '%Y-%m-%d'))
        cls.data = {
            'user': {
                'first_name': cls.first_name,
                'last_name': cls.last_name,
                'email': cls.email,
                'password': cls.password,
            },
            'first_name': cls.first_name,
            'last_name': cls.last_name,
            'dob': cls.dob,
        }
        cls.data2 = deepcopy(cls.data)
        cls.data2['user']['email'] = cls.email2
        cls.delete_user_instance(cls.email)
        cls.delete_user_instance(cls.email2)

    def create_and_login(self, create):
        user = create(self.data)
        self.client.login(**{'email': self.email, 'password': self.password})
        return user

    @classmethod
    def delete_user_instance(cls, email):
        user = User.objects.filter(email__exact=email)
        if user.exists():
            user.delete()

    def tearDown(self):
        self.delete_user_instance(self.email)
        self.delete_user_instance(self.email2)

    @classmethod
    def tearDownClass(cls):
        print('')
        super().tearDownClass()
