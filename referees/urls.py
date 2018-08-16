from django.urls import (
    path,
    re_path
)
from .views import (
    RefereeDetailView,
    RefereeIndexView,
    RefereeLoggerView,
    RefereeExamView
)

app_name = 'referees'

urlpatterns = [
    re_path(
        r'^(?P<slug>([a-z]+)-([a-z]+)(_\d)*)/$',
        RefereeLoggerView.as_view(),
        name='referee logger'
    ),
    re_path(
        r'^logger/(?P<slug>([a-z]+)-([a-z]+)(_\d)*)/$',
        RefereeDetailView.as_view(),
        name='referee detail'
    ),
    path('', RefereeIndexView.as_view(), name='referee home'),
    path('exam/', RefereeExamView.as_view(), name='referee exam'),
]
