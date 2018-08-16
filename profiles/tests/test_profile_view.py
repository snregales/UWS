from django.urls import reverse

from utils.tests.creations import (
    Athlete,
    set_key,
    create_and_activate_athlete as create_athlete,
    create_and_activate_referee as create_referee,
    create_and_activate_both as create_both,
)
from utils.tests.helper import TestHelper
from utils.utils import random_string_generator as gen_key


class ActivateUserView(TestHelper):
    def setup(self, key=None):
        if not key:
            key = set_key(Athlete.objects.create_athlete(**self.data).user)
        self.response = self.client.get(
            reverse(
                'activate',
                kwargs={'code': key}
            ),
        )
        self.assertEqual(self.response.resolver_match.func.__name__, 'ActivateUserView')

    def test_happy_path(self):
        print('happy_path')
        self.setup()
        self.assertRedirects(self.response, reverse('login'), 302)

    def test_bad_link(self):
        print('bad_link')
        self.setup(gen_key())
        self.assertEqual(
            self.response.status_code,
            404  # Not Found
        )


class LoginView(TestHelper):
    def setup(self, create=None):
        if create:
            create(self.data)
        self.response = self.client.post(
            reverse('login'),
            {'email': self.email, 'password': self.password},
            follow=True
        )
        self.assertEqual(self.response.resolver_match.func.__name__, 'LoginView')

    def test_login_a_referee(self):
        print('login_a_referee')
        """
        TODO: must assert that LoginView redirects to referees:referee detail 
        """
        self.setup(create_referee)
        self.assertEqual(
            self.response.status_code,
            200  # OK
        )

    def test_login_a_athlete(self):
        print('login_a_athlete')
        """
        TODO: must assert that LoginView redirects to athletes:athlete detail 
        """
        self.setup(create_athlete)
        self.assertEqual(
            self.response.status_code,
            200  # OK
        )

    def test_user_contain_both_profile(self):
        print('user_contain_both_profile')
        """
        TODO: must assert that LoginView redirects to profile:login choice
        """
        self.setup(create_both)
        self.assertEqual(
            self.response.status_code,
            200  # OK
        )

    def test_logged_user(self):
        print('logged_user')
        self.create_and_login(create_athlete)
        response = self.client.get(reverse('login'))
        self.assertEqual(response.resolver_match.func.__name__, 'LoginView')
        self.assertEqual(
            response.status_code,
            200  # OK
        )
        # self.assertEqual(response.url, reverse('athletes:athlete detail', kwargs={'slug': 'sharlon-regales'}))

    def test_anonymous_user(self):
        print('anonymous_user')
        """
        TODO: must assert that the form raises an Validation Error
        """
        self.setup()
        self.assertEqual(
            self.response.status_code,
            200  # OK
        )


class LoginChoiceView(TestHelper):
    def test_LoginChoiceView_anonymous_user(self):
        print('LoginChoiceView_anonymous_user')
        url = reverse('login choice')
        response = self.client.get(url)
        self.assertEqual(response.resolver_match.func.__name__, 'LoginChoiceView')

        self.assertRedirects(response, reverse('login') + '?next=' + url, 302)

    def test_LoginChoiceView_athlete_user(self):
        print('LoginChoiceView_athlete_user')
        create_athlete(self.data)
        self.client.login(**{'email': self.email, 'password': self.password})
        url = reverse('login choice')
        response = self.client.get(url)
        self.assertEqual(response.resolver_match.func.__name__, 'LoginChoiceView')

        self.assertRedirects(response, reverse('login') + '?next=' + url, 302)

    def test_LoginChoiceView_referee_user(self):
        print('LoginChoiceView_referee_user')
        create_referee(self.data)
        self.client.login(**{'email': self.email, 'password': self.password})
        url = reverse('login choice')
        response = self.client.get(url)
        self.assertEqual(response.resolver_match.func.__name__, 'LoginChoiceView')

        self.assertRedirects(response, reverse('login') + '?next=' + url, 302)

    def test_LoginChoiceView_both(self):
        print('LoginChoiceView_both')
        create_both(self.data)
        self.client.login(**{'email': self.email, 'password': self.password})
        url = reverse('login choice')
        response = self.client.get(url)
        self.assertEqual(response.resolver_match.func.__name__, 'LoginChoiceView')

        self.assertRedirects(response, reverse('login') + '?next=' + url, 302)


class ChangePasswordRequestView(TestHelper):
    def setup(self):
        self.url = reverse('password request')
        self.response = self.client.post(self.url, {'email': self.email})
        self.assertEqual(self.response.resolver_match.func.__name__, 'ChangePasswordRequestView')

    def test_non_existing_user(self):
        print('non_existing_user')
        self.setup()
        self.assertEqual(
            self.response.status_code,
            200  # OK
        )

    def test_logged_user(self):
        print('logged_user')
        self.create_and_login(create_athlete)
        self.setup()
        self.assertRedirects(self.response, reverse('home'), 302)

    def test_happy_path(self):
        print('happy_path')
        create_athlete(self.data)
        self.setup()
        self.assertRedirects(self.response, reverse('login'), 302)


class ValidatePasswordChangeRequestView(TestHelper):
    def setup(self, key=None):
        if not key:
            self.athlete = create_athlete(self.data)
            key = set_key(self.athlete.user)
        url = reverse('pass change prep', kwargs={'slug': 'sharlon-regales', 'code': key})
        self.response = self.client.get(url)
        self.assertEqual(self.response.resolver_match.func.__name__, 'ValidatePasswordChangeRequestView')

    def test_happy_path(self):
        print('happy_path')
        self.setup()
        self.assertRedirects(self.response, reverse('change pass', kwargs={'slug': self.athlete.slug}), 302)

    def test_non_existing_user(self):
        print('non_existing_user')
        self.setup(gen_key())
        self.assertEqual(
            self.response.status_code,
            404  # Not Found
        )

    def test_invalid_code(self):
        print('invalid_code')
        athlete = create_athlete(self.data)
        set_key(athlete.user)
        url = reverse('pass change prep', kwargs={'slug': 'sharlon-regales', 'code': gen_key()})
        with self.assertRaises(LookupError):
            self.client.get(url)

    def test_expired_code(self):
        print('expired_code')
        athlete = create_athlete(self.data)
        set_key(athlete.user)
        import datetime
        from pytz import timezone
        athlete.user.key_date = datetime.datetime.now(timezone('UTC')).replace(microsecond=0) - datetime.timedelta(days=1)
        athlete.user.save()
        url = reverse('pass change prep', kwargs={'slug': 'sharlon-regales', 'code': athlete.user.key})
        with self.assertRaises(LookupError):
            self.client.get(url)

    def test_logged_user(self):
        print('logged_user')
        athlete = self.create_and_login(create_athlete)
        self.setup(set_key(athlete.user))
        self.assertRedirects(self.response, reverse('home'), 302)


class ChangePasswordView(TestHelper):
    def setup(self, login=False):
        if login:
            athlete = self.create_and_login(create_athlete)
        else:
            athlete = create_athlete(self.data)
            set_key(athlete.user, 'Forgot Password')
        url = reverse('change pass', kwargs={'slug': 'sharlon-regales'})
        self.response = self.client.post(url, {'initial': self.password, 'confirm': self.password})
        self.assertEqual(self.response.resolver_match.func.__name__, 'ChangePasswordView')

    def test_logged_user(self):
        print('logged_user')
        self.setup(True)
        self.assertRedirects(self.response, reverse('login'), 302)

    def test_anonymous_user_no_pass_prep(self):
        print('anonymous_user_no_pass_prep')
        athlete = create_athlete(self.data)
        url = reverse('change pass', kwargs={'slug': athlete.slug})
        with self.assertRaises(KeyError):
            self.client.post(url, {'initial': self.password, 'confirm': self.password})

    def test_anonymous_user_pass_prep(self):
        print('anonymous_user_pass_prep')
        self.setup()
        self.assertRedirects(self.response, reverse('login'), 302)

    def test_anonymous_expired(self):
        print('anonymous_expired')
        athlete = create_athlete(self.data)
        set_key(athlete.user, 'Forgot Password')
        import datetime
        from pytz import timezone
        athlete.user.key_date = datetime.datetime.now(timezone('UTC')).replace(microsecond=0) - datetime.timedelta(days=1)
        athlete.user.save()
        url = reverse('change pass', kwargs={'slug': athlete.slug})
        with self.assertRaises(KeyError):
            self.client.post(url, {'initial': self.password, 'confirm': self.password})