from django.views import generic
from profiles.views import (
    UserPassesTestMixin,
    ProfileDetailView as Detail,
    RegisterView as Register,
)
from scheduler.models.matches import Match
from .forms import RefereeRegistrationForm, ExamForm, Referee


##########################################################################################


def authenticate_user(user):
    return user.is_authenticated and user.is_referee


class RefereePassesTest(UserPassesTestMixin):
    def test_func(self):
        return authenticate_user(self.request.user)


class LogRefereePassedTest(UserPassesTestMixin):
    def test_func(self):
        if authenticate_user(self.request.user):
            # Do something
            pass
        return False


class RefereeDetailView(RefereePassesTest, Detail):
    template_name = 'referee_detail.html'


class RefereeIndexView(RefereePassesTest, generic.TemplateView):
    template_name = 'referee_home.html'


##########################################################################################


class RefereeRegisterView(Register):
    form_class = RefereeRegistrationForm
    success_message = "Your referee account was created successfully. Please check your email."
    extra_context = {
        'title': 'Sign Up',
        'heading': 'Referee Sign Up',
        'buttons': [('sign_up', 'Sign Up')],
    }


class RefereeLoggerView(RefereePassesTest, generic.UpdateView):
    # TODO: create model Team to use
    template_name = 'logger.html'
    model = Match


class RefereeExamView(RefereePassesTest, generic.UpdateView):
    form_class = ExamForm
    model = Referee
    template_name = 'snippets/form.html'
    extra_context = {
        'title': 'Exam',
        'heading': 'Referee Examination',
        'buttons': [('finish', 'Finished')],
    }

    def form_valid(self, form):
        if form.clean_data['examination'] == 'Pass':
            form.clean_data.update({'certified': True})
        return super(RefereeExamView, self).form_valid(form)
