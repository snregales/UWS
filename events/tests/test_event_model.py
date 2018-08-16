from djongo.sql2mongo import SQLDecodeError

from .shedule_helper import EventTestHelper, timedelta
from ..models import EventMeta


class EventModel(EventTestHelper):
    def setUp(self):
        self.event, self.meta = EventMeta.objects.create_event(self.name, self.date, **self.model_meta)

    def test_create_event(self):
        print('create_event')
        self.assertEqual(self.event.slug, self.event_slug)
        self.assertEqual(self.meta.type, self.model_meta['type'])

    def test_create_event_duplicate_event(self):
        print('create_event_duplicate_event')
        with self.assertRaises(SQLDecodeError):
            EventMeta.objects.create_event(self.name, self.date, **self.model_meta)

    def test_create_event_same_names_dif_dates(self):
        print('create_event_same_name_dif_dates')
        event, meta = EventMeta.objects.create_event(self.name, self.date + timedelta(days=367), **self.model_meta)
        self.assertNotEqual(event, self.event)
        self.assertEqual(event.slug, 'some-event-name_20')

    def test_create_event_same_dates_dif_names(self):
        print('create_event_same_dates_dif_names')
        event, meta = EventMeta.objects.create_event('Some Other Event', self.date, **self.model_meta)
        self.assertNotEqual(event, self.event)
        self.assertEqual(event.slug, 'some-other-event_19')

    def test_add_team_to_event(self):
        print('add_team_to_event')
        self.create_teams(2)
        self.assertFalse(self.meta.teams.all())
        self.meta.add_team_to_event(self.team_list[0])
        self.assertQuerysetEqual(self.meta.teams.all(), ['<Team: C>'])
        del self.team_list[0]
        self.meta.add_team_to_event(self.team_list)
        self.assertQuerysetEqual(self.meta.teams.all(), ['<Team: A>', '<Team: B>', '<Team: C>'])
