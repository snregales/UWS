from django.urls import reverse

from utils.tests.helper import TestHelper, User
from utils.tests.creations import (
    create_and_activate_referee as create_referee,
    create_and_activate_athlete as create_athlete
)


class RefereeView(TestHelper):
    def test_RegisterView(self):
        print('RefereeRegisterView')
        response = self.client.post(reverse('referee register'), self.data)
        self.assertEqual(
            response.status_code,
            200  # OK
        )

    def test_RefereeIndexView_logged_user(self):
        print('RefereeIndexView_logged_user')
        referee = create_referee(self.data)
        url = reverse('referees:referee home')
        self.client.login(**{'email': self.email, 'password': self.password})
        response = self.client.get(url)
        self.assertEqual(
            response.status_code,
            200  # OK
        )

    def test_RefereeIndexView_anonymous(self):
        print('RefereeIndexView_anonymous')
        url = reverse('referees:referee home')
        response = self.client.get(url)
        self.assertEqual(
            response.status_code,
            302  # Redirect
        )
        self.assertRedirects(response, reverse('login') + '?next=' + url)

    def test_RefereeIndexView_logged_non_referee_user(self):
        print('RefereeIndexView_logged_non_referee_user')
        athlete = create_athlete(self.data)
        self.client.login(**{'email': self.email, 'password': self.password})
        url = reverse('referees:referee home')
        response = self.client.get(url)
        self.assertEqual(
            response.status_code,
            302  # Redirect
        )
        self.assertRedirects(response, reverse('login') + '?next=' + url)

    def test_RefereeDetailView_anonymous(self):
        print('RefereeDetailView_anonymous')
        url = reverse('referees:referee detail', kwargs={'slug': 'sharlon-regales'})
        response = self.client.get(url)
        self.assertEqual(
            response.status_code,
            302  # Redirect
        )
        self.assertRedirects(response, reverse('login') + '?next=' + url)

    def test_RefereeDetailView_logged_non_referee_user(self):
        print('RefereeDetailView_logged_non_referee_user')
        athlete = create_athlete(self.data)
        self.client.login(**{'email': self.email, 'password': self.password})
        url = reverse('referees:referee detail', kwargs={'slug': athlete.slug})
        response = self.client.get(url)
        self.assertEqual(
            response.status_code,
            302  # Redirect
        )
        self.assertRedirects(response, reverse('login') + '?next=' + url)

    def test_RefereeDetailView_logged_user(self):
        print('RefereeDetailView_logged_user')
        referee = create_referee(self.data)
        url = reverse('referees:referee detail', kwargs={'slug': referee.slug})
        self.client.login(**{'email': self.email, 'password': self.password})
        response = self.client.get(url)
        self.assertEqual(
            response.status_code,
            200  # OK
        )

    def test_RefereeLoggerView_anonymous(self):
        print('RefereeLoggerView_anonymous')
        url = reverse('referees:referee logger', kwargs={'slug': 'sharlon-regales'})
        response = self.client.get(url)
        self.assertEqual(response.resolver_match.func.__name__, 'RefereeLoggerView')
        self.assertEqual(
            response.status_code,
            302  # Redirect
        )
        self.assertRedirects(response, reverse('login') + '?next=' + url)

    def test_RefereeLoggerView_logged_non_referee_user(self):
        print('RefereeLoggerView_logged_non_referee_user')
        athlete = create_athlete(self.data)
        self.client.login(**{'email': self.email, 'password': self.password})
        url = reverse('referees:referee logger', kwargs={'slug': athlete.slug})
        response = self.client.get(url)
        self.assertEqual(response.resolver_match.func.__name__, 'RefereeLoggerView')
        self.assertEqual(
            response.status_code,
            302  # Redirect
        )
        self.assertRedirects(response, reverse('login') + '?next=' + url)

    def test_RefereeLoggerView_logged_user(self):
        # FAIL: Because there is no proper Team model yet
        print('RefereeLoggerView_logged_user')
        referee = create_referee(self.data)
        url = reverse('referees:referee logger', kwargs={'slug': referee.slug})
        self.client.login(**{'email': self.email, 'password': self.password})
        response = self.client.get(url)
        self.assertEqual(response.resolver_match.func.__name__, 'RefereeLoggerView')
        self.assertEqual(
            response.status_code,
            200  # OK
        )
