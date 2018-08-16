import operator
from functools import reduce
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse
from django.views import generic
from djongo.models import Q

from utils.search import SearchMixin
from .forms import (
    AddTeamForm,
    Event,
    EventForm,
)


class AdminPassedTest(UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        return user.is_authenticated and user.is_admin


class StaffPassedTest(UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        return user.is_authenticated and user.is_staff


class CreateEventView(AdminPassedTest, generic.CreateView):
    form_class = EventForm
    template_name = 'snippets/form.html'
    extra_context = {
        'title': 'Create Event',
        'heading': 'Create Event',
        'buttons': [
            ('create', 'Create'),
            ('cancel', 'Cancel')
        ]
    }

    def post(self, request, *args, **kwargs):
        from django.shortcuts import HttpResponseRedirect
        if 'cancel' in request.POST:
            return HttpResponseRedirect(self.get_success_url())
        return super(CreateEventView, self).post(request, *args, **kwargs)

    def get_success_url(self):
        event, meta = self.object
        return reverse('events:detail', kwargs={'slug': event.slug})


# TODO:fix UpdateView
# problem: NoneType error object has no attribute attname
# solution: don't use EventForm or EventForm's validations
class UpdateEventView(StaffPassedTest, generic.UpdateView):
    form_class = EventForm
    model = Event
    template_name = 'snippets/form.html'
    extra_context = {
        'title': 'Update Event',
        'heading': 'Update Event',
        'buttons': [
            ('update', 'Update'),
            ('cancel', 'Cancel')
        ]
    }

    def post(self, request, *args, **kwargs):
        from django.shortcuts import HttpResponseRedirect
        if 'cancel' in request.POST:
            return HttpResponseRedirect(self.get_success_url())
        return super(UpdateEventView, self).post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('events:detail', kwargs={'slug': self.object.slug})


class AddTeamToEventView(StaffPassedTest, generic.FormView):
    form_class = AddTeamForm
    template_name = 'snippets/form.html'
    extra_context = {
        'title': 'Add Team',
        'heading': 'Add Team to Event',
        'buttons': [
            ('add_more', 'Save and Add More'),
            ('quite', 'Save and Quite'),
            ('cancel', 'Cancel'),
        ]
    }

    def get_form_kwargs(self):
        kwargs = super(AddTeamToEventView, self).get_form_kwargs()
        kwargs.update({'slug': self.kwargs['slug']})
        return kwargs

    def post(self, request, *args, **kwargs):
        from django.shortcuts import HttpResponseRedirect
        if 'cancel' in request.POST:
            return HttpResponseRedirect(self.get_success_url())
        return super(AddTeamToEventView, self).post(request, *args, **kwargs)

    # TODO: decline to add team to event that already closed
    def form_valid(self, form):
        from django.shortcuts import get_object_or_404, HttpResponseRedirect
        event = get_object_or_404(Event, slug=self.kwargs['slug']).eventmeta
        event.add_team_to_event(form.cleaned_data['teams'])
        event.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        form = self.get_form_kwargs()
        if 'add_more' in form['data']:
            return reverse('events:add team to event', kwargs=self.kwargs)
        return reverse('events:event home')


class EventListView(generic.ListView, SearchMixin):
    """
    Display a list of Events filter by the search query
    if empty display all events
    """
    model = Event
    template_name = 'index_event.html'
    paginate_by = 25

    def get_queryset(self):
        result = super(EventListView, self).get_queryset()
        queryset = self.request.GET.get('search')
        if not queryset:
            return result

        query_list = queryset.split()
        result = result.filter(
            reduce(operator.and_,
                   (Q(name__icontains=q) for q in query_list)) |
            reduce(operator.and_,
                   (Q(type__icontains=q) for q in query_list))
        )
        return result


class EventDetailView(generic.DetailView):
    model = Event
    template_name = 'event_detail.html'
