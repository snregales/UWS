from django.urls import re_path

from .views import (
    AthleteDetailView,
)

app_name = 'athletes'

urlpatterns = [
    # slug should be as follow firstname-lastname(_sw) 0 or more time all lowercase
    # regex for slug look like ^([a-z]+)-([a-z]+)(_\d)*$
    # regex for code look like ^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)([^\W^_]{32})$
    re_path(
        r'^(?P<slug>([a-z]+)-([a-z]+)(_\d)*)/$',
        AthleteDetailView.as_view(),
        name='athlete detail'
    ),
]
