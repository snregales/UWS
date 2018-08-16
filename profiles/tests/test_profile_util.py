from profiles.utils import (
    create_unique_id,
    send_activation_email,
)
from utils.tests.creations import (
    Athlete,
    Referee,
    activate_user,
)
from utils.tests.helper import (
    TestHelper,
    User,
)


class ProfileUtil(TestHelper):
    def test_activate_user(self):
        print('activate_user')
        athlete = Athlete.objects.create_athlete(**self.data)
        self.assertFalse(athlete.user.is_active)
        self.assertNotEqual(athlete.user.key, '')
        activate_user(athlete.user)
        self.assertTrue(athlete.user.is_active)
        self.assertFalse(athlete.user.key)

    def test_create_unique_id(self):
        print('create_unique_id')
        athlete = Athlete.objects.create_athlete(**self.data)
        self.assertNotEqual(
            create_unique_id(athlete),
            create_unique_id(athlete)
        )
        self.assertNotEqual(
            create_unique_id(athlete),
            athlete.id
        )
        if 'dob' in self.data2:
            del self.data2['dob']
        referee = Referee.objects.create_referee(**self.data2)
        self.assertNotEqual(
            create_unique_id(referee),
            referee.id
        )
        self.assertNotEqual(
            referee.id,
            athlete.id,
        )

    def test_send_activation_email(self):
        print('send_activation_email')
        self.delete_user_instance(self.email)
        user = User.objects.create_user(**self.data['user'])
        self.assertFalse(user.is_active and user.key)
        self.assertEqual(
            send_activation_email(user),
            'localhost:8000/activate/' + user.key + '/'
        )
