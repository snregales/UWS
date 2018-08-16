from django.views.generic import FormView
from events.views import AdminPassedTest
from django.urls import reverse_lazy, reverse
from django import forms
from .systems.events import Scheduler

class ButtonForm(forms.Form):
    box = forms.CharField(label='', initial='box', widget=forms.TextInput(attrs={'hidden': True}))

class ScheduleButtonView(FormView, AdminPassedTest):
    template_name = 'snippets/form.html'
    form_class = ButtonForm
    success_url = reverse_lazy('home')
    extra_context = {
        'title': 'Book',
        'heading': 'Schedule Event',
        'buttons': [
            ('schedule', 'Schedule Event'),
            ('cancel', 'Cancel'),
        ]
    }

    def post(self, request, *args, **kwargs):
        from django.shortcuts import HttpResponseRedirect
        if 'cancel' in request.POST:
            return HttpResponseRedirect(self.get_success_url())
        scheduler = Scheduler()
        scheduler.schedule_events()
        return super(ScheduleButtonView, self).post(request, *args, **kwargs)

    def get_success_url(self):
        form = self.get_form_kwargs()
        if 'schedule' in form['data']:
            return reverse('events:event home')
        return super(ScheduleButtonView, self).get_success_url()
