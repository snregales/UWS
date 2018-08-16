from utils.tests.helper import TestHelper, User
from ..utils import create_unique_slug


class AccountUtil(TestHelper):
    def setUp(self):
        self.user = User.objects.create_user(
            **self.data['user']
        )

    def test_create_unique_slug(self):
        print('create_unique_slug')
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(self.user.slug, 'sharlon-regales')
        self.assertNotEqual(
            create_unique_slug(self.user.__class__, **self.data),
            self.user.slug
        )
        del self.data['first_name']
        del self.data['last_name']
        with self.assertRaises(KeyError):
            create_unique_slug(self.user.__class__, **self.data)
        self.data.update({'staff_alias': 'kalonji'})
        self.assertEqual(
            create_unique_slug(self.user.__class__, **self.data),
            'staff-kalonji'
        )
        self.data.update({'admin_alias': 'kalonji'})
        del self.data['staff_alias']
        self.assertEqual(
            create_unique_slug(self.user.__class__, **self.data),
            'admin-kalonji'
        )
