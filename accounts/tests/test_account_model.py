from accounts.models import User
from utils.tests.helper import TestHelper


class TestUserModel(TestHelper):
    def test_no_privilege_user(self):
        print('no_privilege_user')
        user = User.objects.create_user(
            **self.data['user']
        )
        self.assertFalse(
            (user.is_active
             and user.is_referee and user.is_staff
             and user.is_admin and user.is_athlete)
        )

    def test_staff_privileges(self):
        print('staff_privileges')
        user = User.objects.create_staff(
            **self.data['user']
        )
        self.assertTrue(
            (not (user.is_active or user.is_referee
                  or user.is_admin or user.is_athlete)
             and user.is_staff
             )
        )

    def test_super_privileges(self):
        print('super_privileges')
        user = User.objects.create_superuser(
            **self.data['user']
        )
        self.assertTrue(
            not (user.is_referee or user.is_athlete)
            and user.is_staff and user.is_active
            and user.is_admin
        )

    def test_referee_privileges(self):
        print('referee_privileges')
        user = User.objects.create_referee(
            **self.data['user']
        )
        self.assertTrue(
            (not (user.is_staff or user.is_active
                  or user.is_admin or user.is_athlete
                  )
             and user.is_referee
             )
        )

    def test_athlete_privileges(self):
        print('referee_privileges')
        user = User.objects.create_athlete(
            **self.data['user']
        )
        self.assertTrue(
            (not (user.is_staff or user.is_active
                  or user.is_admin or user.is_referee
                  )
             and user.is_athlete
             )
        )

    def test_user_empty_fields(self):
        print('user_empty_fields')
        with self.assertRaises(ValueError):
            my_data = self.data.copy()
            my_data['email'] = ''
            User.objects.create_user(
                **my_data
            )
            del my_data['email']
            User.objects.create_user(
                **my_data
            )
            my_data = self.data.copy()
            my_data['initial'] = ''
            User.objects.create_user(
                **my_data
            )
            del my_data['initial']
            User.objects.create_user(
                **my_data
            )
            my_data = self.data.copy()
            my_data['confirm'] = ''
            User.objects.create_user(
                **my_data
            )
            del my_data['confirm']
            User.objects.create_user(
                **my_data
            )
