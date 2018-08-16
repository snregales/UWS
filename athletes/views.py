from profiles.views import (
    ProfileDetailView as Detail,
    RegisterView as Register,
    UserPassesTestMixin,
)
from .forms import AthleteRegisterForm


###############################################################################################


class AthletePassesTest(UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        if not user.is_authenticated:
            return False
        return user.is_athlete


class AthleteDetailView(AthletePassesTest, Detail):
    template_name = 'athlete_detail.html'


###############################################################################################


class AthleteRegisterView(Register):
    form_class = AthleteRegisterForm
    success_message = "Your athlete account was created successfully. Please check your email."
    extra_context = {
        'title': 'Sign Up',
        'heading': 'Athlete Sign Up',
        'buttons': [('sign_up', 'Sign Up')],
    }
