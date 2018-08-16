from django.contrib.auth.views import LogoutView
from django.urls import (
    include,
    path,
    re_path
)
from django.views.generic import TemplateView
from profiles.views import (
    ActivateUserView,
    ChangePasswordView,
    ChangePasswordRequestView,
    LoginChoiceView,
    LoginView,
    ValidatePasswordChangeRequestView,
)
from athletes.views import AthleteRegisterView
from referees.views import RefereeRegisterView


urlpatterns = [
    re_path(
        r'^activate/(?P<code>(?=.*[a-z])(?=.*[A-Z])(?=.*\d)([^\W^_]{32}))/$',
        ActivateUserView.as_view(),
        name='activate'
    ),
    re_path(
        r'^chng-pass/(?P<slug>([a-z]+)-([a-z]+)(_\d)*)/$',
        ChangePasswordView.as_view(),
        name='change pass'
    ),
    re_path(
        r'^chng-pass-req/(?P<slug>([a-z]+)-([a-z]+)(_\d)*)/(?P<code>(?=.*[a-z])(?=.*[A-Z])(?=.*\d)([^\W^_]{32}))/$',
        ValidatePasswordChangeRequestView.as_view(),
        name='pass change prep'
    ),

    # path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('login-choice/', LoginChoiceView.as_view(), name='login choice'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('sign-up/', TemplateView.as_view(template_name='registration/signup_choice.html'), name='sign-up choice'),
    path('sign-up-ath/', AthleteRegisterView.as_view(), name='athlete register'),
    path('sign-up-ref/', RefereeRegisterView.as_view(), name='referee register'),
    path('req-pass-chng/', ChangePasswordRequestView.as_view(), name='password request'),

    path('athlete/', include('athletes.urls')),
    path('event/', include('events.urls')),
    path('ref/', include('referees.urls')),
    path('book/', include('scheduler.urls')),
    path('team/', include('teams.urls')),
]
