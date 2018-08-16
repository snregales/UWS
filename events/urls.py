from django.urls import path, re_path

from .views import (
    CreateEventView,
    UpdateEventView,
    AddTeamToEventView,
    EventDetailView,
    EventListView,
)

app_name = 'events'

urlpatterns = [
    re_path(
        r'^(?P<slug>(([a-z]+-?)+_([\d]{2})))/add/$',
        AddTeamToEventView.as_view(),
        name='add team to event'
    ),
    re_path(
        r'^(?P<slug>(([a-z]+-?)+_([\d]{2})))/$',
        EventDetailView.as_view(),
        name='detail'
    ),
    re_path(
        r'^(?P<slug>(([a-z]+-?)+_([\d]{2})))/update/',
        UpdateEventView.as_view(),
        name='update event'
    ),
    path('', EventListView.as_view(), name='event home'),
    path('create/', CreateEventView.as_view(), name='create event'),
]
