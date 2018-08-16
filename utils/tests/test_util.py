from .helper import TestHelper, User
from ..utils import *


class UtilUtil(TestHelper):
    def test_random_string_generator(self):
        print('random_string_generator')
        rand = random_string_generator()
        self.assertEqual(rand.__len__(), 32)
        self.assertNotEqual(rand, random_string_generator())
        self.assertEqual(random_string_generator(5).__len__(), 5)

    def test_set_key(self):
        print('set_key')
        user = User.objects.create_user(
            **self.data['user']
        )
        self.assertFalse(user.key)
        self.assertFalse(user.is_active)
        key = set_key(user)
        self.assertEqual(key, user.key)
        self.assertFalse(user.is_active)

    # def test_choice_list(self):
    #     print('choice_list')
    #     User.objects.create_user(self.email, self.password)
    #     a_list = choice_list(User)
    #     self.assertEqual(a_list.count(), 1)

    def test_assert_slug_unique(self):
        print('assert_slug_unique')
        user = User.objects.create_user(
            **self.data['user']
        )
        self.assertNotEqual(
            assert_slug_unique(user.slug, user.__class__),
            user.slug
        )
        self.assertNotEqual(
            assert_slug_unique(DONT_SLUG.__getitem__(0), User),
            DONT_SLUG.__getitem__(0)
        )
