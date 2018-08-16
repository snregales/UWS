from django.urls import path, re_path

from .views import (
    AddTeam,
    TeamList,
    TeamUpdate
)

app_name = 'teams'

urlpatterns = [
    path('', TeamList.as_view(), name='home'),
    path('add/', AddTeam.as_view(), name='add'),
    re_path(
        r'^(?P<slug>(([a-z]+-?)+))/$',
        TeamUpdate.as_view(),
        name='update'
    ),
]

