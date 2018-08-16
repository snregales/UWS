from django.urls import path
from .views import ScheduleButtonView

app_name = 'scheduler'

urlpatterns = [
    path('', ScheduleButtonView.as_view(), name='schedule'),
]