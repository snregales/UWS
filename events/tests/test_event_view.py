from .shedule_helper import EventTestHelper
from ..views import reverse
from utils.tests.creations import (
    create_and_activate_admin,
    create_and_activate_user,
)


class CreateEventView(EventTestHelper):
    def setup(self):
        self.url = reverse('events:create event')
        self.response = self.client.post(self.url)
        self.assertEqual(self.response.resolver_match.func.__name__, 'CreateEventView')

    def test_anonymous_user(self):
        print('anonymous_user')
        self.setup()
        self.assertRedirects(self.response, reverse('login')+'?next='+self.url, 302)

    def test_non_admin_user(self):
        print('non_admin_user')
        self.create_and_login(create_and_activate_user)
        self.setup()
        self.assertRedirects(self.response, reverse('login')+'?next='+self.url, 302)

    def test_happy_path(self):
        print('happy_path')
        self.create_and_login(create_and_activate_admin)
        self.setup()
        self.assertEqual(
            self.response.status_code,
            200
        )


class UpdateEventView(EventTestHelper):
    def setup(self):
        self.url = reverse('events:update event', kwargs={'slug': self.event_slug})
        self.response = self.client.post(self.url)
        self.assertEqual(self.response.resolver_match.func.__name__, 'UpdateEventView')

    def test_anonymous_user(self):
        print('anonymous_user')
        self.setup()
        self.assertRedirects(self.response, reverse('login')+'?next='+self.url, 302)

    def test_staff_user(self):
        print('non_staff_user')
        self.create_and_login(create_and_activate_user)
        self.setup()
        self.assertRedirects(self.response, reverse('login')+'?next='+self.url, 302)

    def test_happy_path(self):
        print('happy_path')
        from events.models import EventMeta
        self.create_and_login(create_and_activate_admin)
        EventMeta.objects.create_event(self.name, self.date, **self.model_meta)
        self.setup()
        self.assertEqual(
            self.response.status_code,
            200
        )


class AddTeamToEventView(EventTestHelper):
    def setup(self, data=None, follow=False):
        self.url = reverse('events:add team to event', kwargs={'slug': self.event_slug})
        self.response = self.client.post(self.url, data=data, follow=follow)
        self.assertEqual(self.response.resolver_match.func.__name__, 'AddTeamToEventView')

    def test_anonymous_user(self):
        print('anonymous_user')
        self.setup()
        self.assertRedirects(self.response, reverse('login')+'?next='+self.url, 302)

    def test_non_staff_user(self):
        print('non_staff_user')
        self.create_and_login(create_and_activate_user)
        self.setup()
        self.assertRedirects(self.response, reverse('login')+'?next='+self.url, 302)

    def test_AddTeamToEventView_save_add_more(self):
        print('AddTeamToEventView_save_add_more')
        self.create_and_login(create_and_activate_admin)
        data = self.meta_form.copy()
        data.update({'add_more': 'Save and Add More'})
        self.setup(data, True)
        self.assertEqual(self.response.status_code, 200)

    def test_AddTeamToEventView_save_add_quit(self):
        print('AddTeamToEventView_save_add_quit')
        self.create_and_login(create_and_activate_admin)
        data = self.meta_form.copy()
        data.update({'quite': 'Save and Quite'})
        self.setup(data, True)
        self.assertEqual(self.response.status_code, 200)