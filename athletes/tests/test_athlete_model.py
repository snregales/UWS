from ..models import Athlete
from utils.tests.helper import TestHelper, User


class AthleteModel(TestHelper):
    def setUp(self):
        self.profile = Athlete.objects.create_athlete(**self.data)

    def test_athlete_model_qs(self):
        print('profile_model_qs')
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(Athlete.objects.count(), 1)
        self.assertFalse(self.profile.user.is_active)

    def test_create_profile_existing_user(self):
        print('create_profile_existing_user')
        with self.assertRaises(ValueError):
            Athlete.objects.create_athlete(**self.data)

    def test_slug_field(self):
        print('slug_field')
        self.assertEqual(User.objects.count(), 1)
        profile = Athlete.objects.create_athlete(**self.data2)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(profile.__str__, self.profile.__str__)
        self.assertNotEqual(profile.user.slug, self.profile.user.slug)
        self.delete_user_instance(profile.user.email)
