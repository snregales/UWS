from django.views import generic
from django.urls import reverse
from django.contrib.auth.mixins import UserPassesTestMixin

from .models import Team, TeamCreateForm, TeamUpdateForm


class AdminPassedTest(UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        if not user.is_authenticated:
            return False
        return user.is_admin


class AddTeam(AdminPassedTest, generic.CreateView):
    form_class = TeamCreateForm
    template_name = 'snippets/form.html'
    extra_context = {
        'title': 'Add Team',
        'heading': 'Add Team To System',
        'buttons': [
            ('add_more', 'Save and Add More'),
            ('quite', 'Save and Quite'),
            ('cancel', 'Cancel')
        ]
    }

    def post(self, request, *args, **kwargs):
        from django.shortcuts import HttpResponseRedirect
        if 'cancel' in request.POST:
            return HttpResponseRedirect(self.get_success_url())
        return super(AddTeam, self).post(request, *args, **kwargs)

    def get_success_url(self):
        form = self.get_form_kwargs()
        if 'add_more' in form['data']:
            return reverse('teams:add')
        return reverse('teams:home')


class TeamList(generic.ListView):
    model = Team
    template_name = 'index_teams.html'


class TeamUpdate(AdminPassedTest, generic.UpdateView):
    model = Team
    form_class = TeamUpdateForm
    redirect_field_name = 'teams:home'
    template_name = 'snippets/form.html'
    extra_context = {
        'title': 'Update Team',
        'heading': 'Update Team',
        'buttons': [
            ('update', 'Update'),
            ('cancel', 'Cancel')
        ]
    }

    def post(self, request, *args, **kwargs):
        from django.shortcuts import HttpResponseRedirect
        if 'cancel' in request.POST:
            return HttpResponseRedirect(self.get_success_url())
        return super(TeamUpdate, self).post(request, *args, **kwargs)

