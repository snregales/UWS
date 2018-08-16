from django.urls import reverse

from utils.tests.helper import TestHelper, User
from utils.tests.creations import (
    create_and_activate_referee as create_referee,
    create_and_activate_athlete as create_athlete
)


class AthleteView(TestHelper):
    def test_RegisterView(self):
        print('AthleteRegisterView')
        response = self.client.post(reverse('athlete register'), self.data)
        self.assertEqual(
            response.status_code,
            200  # OK
        )

    def test_AthlleteDetailView_anonymous(self):
        print('AthleteDetailView_anonymous')
        url = reverse('athletes:athlete detail', kwargs={'slug': 'sharlon-regales'})
        response = self.client.get(url)
        self.assertEqual(
            response.status_code,
            302  # OK
        )
        self.assertRedirects(response, reverse('login') + '?next=' + url)

    def test_AthleteDetailView_logged_non_referee_user(self):
        print('AthleteDetailView_logged_non_referee_user')
        referee = create_referee(self.data)
        self.client.login(**{'email': self.email, 'password': self.password})
        url = reverse('athletes:athlete detail', kwargs={'slug': referee.slug})
        response = self.client.get(url)
        self.assertEqual(
            response.status_code,
            302  # Redirect
        )
        self.assertRedirects(response, reverse('login') + '?next=' + url)

    def test_AthlleteDetailView_logged_user(self):
        print('AthleteDetailView_logged_user')
        athlete = create_athlete(self.data)
        url = reverse('athletes:athlete detail', kwargs={'slug': athlete.slug})
        self.client.login(**{'email': self.email, 'password': self.password})
        response = self.client.get(url)
        self.assertEqual(
            response.status_code,
            200  # OK
        )
