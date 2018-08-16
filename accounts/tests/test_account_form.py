from utils.tests.helper import TestHelper
from accounts.forms import (
    UserAdminCreationForm,
    UserStaffCreationForm,
    User
)


class AccountForm(TestHelper):
    def setUp(self):
        self.user = self.data['user']
        self.user.update({
            'admin_alias': 'kalonji',
            'staff_alias': 'kalonji',
            'initial': self.user['password'],
            'confirm': self.user['password'],
        })

    def test_UserAdminCreationForm(self):
        print('UserAdminCreationForm')
        form = UserAdminCreationForm(data=self.user)
        self.assertTrue(form.is_valid())
        form.save()
        self.assertTrue(User.objects.filter(slug='admin-kalonji').exists())

    def test_UserStaffCreationForm(self):
        print('UserStaffCreationForm')
        form = UserStaffCreationForm(data=self.user)
        self.assertTrue(form.is_valid())
        form.save()
        self.assertTrue(User.objects.filter(slug='staff-kalonji').exists())

    def test_existing_user__admin_create_form(self):
        print('existing_user')
        User.objects.create_user(**self.data['user'])
        form = UserAdminCreationForm(data=self.data)
        self.assertFalse(form.is_valid())

    def test_miss_data_field(self):
        print('miss_data_field')
        miss_data = self.user.copy()
        miss_data['email'] = ''
        self.assertFalse(UserAdminCreationForm(miss_data).is_valid())
        miss_data = self.user.copy()
        miss_data['confirm'] = ''
        self.assertFalse(UserAdminCreationForm(miss_data).is_valid())
        miss_data = self.user.copy()
        miss_data['initial'] = ''
        self.assertFalse(UserAdminCreationForm(miss_data).is_valid())
