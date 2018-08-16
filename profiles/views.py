from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.views import (
    LoginView as Login,
    resolve_url,
    reverse,
    reverse_lazy,
)
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404
from django.views import generic

from .forms import (
    PasswordChangeForm,
    PasswordChangeRequestForm,
    User,
)
from .utils import activate_user
from utils.utils import (
    is_key_valid,
    password_change_prep,
    send_request_email,
)


class ProfileDetailView(generic.DetailView):
    login_url = reverse_lazy('login')
    model = User


class RegisterView(SuccessMessageMixin, generic.CreateView):
    template_name = 'snippets/form.html'
    success_url = reverse_lazy('login')


########################################################################################


class ActivateUserView(generic.RedirectView):
    pattern_name = 'login'

    def get(self, request, code=None, *args, **kwargs):
        if code:
            user = get_object_or_404(User, key=code)
            activate_user(user)
        return super(ActivateUserView, self).get(request, *args, **kwargs)


class LoginView(Login):
    # redirect_authenticated_user = True
    template_name = 'snippets/form.html'
    extra_context = {
        'title': 'Sign In',
        'heading': 'Sign In',
        'login': True,
        'buttons': [('sign_in', 'Sign In')]
    }

    def get_success_url(self):
        user = self.request.user
        if not user.is_referee and user.is_athlete:
            return self.get_redirect_url() or resolve_url(
                'athletes:athlete detail',
                slug=self.request.user.slug
            )
        if user.is_referee and not user.is_athlete:
            return self.get_redirect_url() or resolve_url(
                'referees:referee detail',
                slug=self.request.user.slug
            )
        if not (user.is_referee or user.is_athlete):
            return self.get_redirect_url() or resolve_url(
                'home'
            )
        return self.get_redirect_url() or resolve_url(
            'login choice'
        )


class LoginChoiceView(UserPassesTestMixin, generic.TemplateView):
    template_name = 'registration/login_choice.html'

    def test_func(self):
        user = self.request.user
        if not user.is_authenticated:
            return False
        return user.is_athlete and user.is_referee


#########################################################################################


class ChangePasswordRequestView(UserPassesTestMixin, SuccessMessageMixin, generic.FormView):
    success_message = "We've emailed you instructions for resetting your password, if an account exists with the email you entered.\
                       \nYou should receive them shortly."
    form_class = PasswordChangeRequestForm
    template_name = 'snippets/form.html'
    success_url = reverse_lazy('login')
    extra_context = {
        'title': 'Pass Reset',
        'heading': 'Password Reset',
        'buttons': [('send', 'Send')]
    }

    def form_valid(self, form):
        user = get_object_or_404(User, email=form.cleaned_data['email'])
        send_request_email(user)
        return super(ChangePasswordRequestView, self).form_valid(form)

    def test_func(self):
        return self.request.user.is_anonymous

    def get_redirect_field_name(self):
        if self.request.user.is_authenticated:
            return reverse_lazy('home')

    def handle_no_permission(self):
        if self.raise_exception:
            from django.core.exceptions import PermissionDenied
            raise PermissionDenied(self.get_permission_denied_message())
        from django.http import HttpResponseRedirect
        return HttpResponseRedirect(resolve_url(self.get_redirect_field_name()))


class ValidatePasswordChangeRequestView(generic.RedirectView):
    pattern_name = 'change pass'

    def get_redirect_url(self, *args, **kwargs):
        if not self.request.user.is_anonymous:
            return reverse('home')
        user = get_object_or_404(User, slug=self.kwargs['slug'])
        if is_key_valid(user, kwargs['code']):
            password_change_prep(user)
        else:
            # TODO: change to send a message to user instead of a LookupError
            raise LookupError('Key is not valid')
        return super(ValidatePasswordChangeRequestView, self).get_redirect_url(slug=kwargs['slug'])


class ChangePasswordView(SuccessMessageMixin, generic.FormView):
    # TODO: ChangePasswordView should display Old Password input if the user is_authenticated
    success_url = reverse_lazy('login')
    success_message = "Password Successfully Changed"
    form_class = PasswordChangeForm
    template_name = 'snippets/form.html'
    extra_context = {
        'title': 'Pass Reset',
        'heading': 'Change Password',
        'button': [
            ('change', 'Change'),
            ('cancel', 'Cancel')
        ]
    }

    def post(self, request, *args, **kwargs):
        from django.shortcuts import HttpResponseRedirect
        if 'cancel' in request.POST:
            return HttpResponseRedirect(self.get_success_url())
        return super(ChangePasswordView, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        if 'forgot_password' not in self.get_context_data() and self.request.user.is_anonymous:
            # TODO: change to send a message to user instead of a KeyError
            raise KeyError('forgot_password not found')
        user = get_object_or_404(User, slug=self.kwargs['slug'])
        user.set_password(form.cleaned_data['initial'])
        user.key = None
        user.save()
        return super(ChangePasswordView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        user = self.get_user()
        context = super(ChangePasswordView, self).get_context_data(**kwargs)
        if is_key_valid(user, 'Forgot Password'):
            context['forgot_password'] = True
        return context

    def get_user(self):
        return User.objects.get_user_instance_slug(self.kwargs['slug'])
