from ..utils import set_key
from athletes.models import Athlete
from profiles.utils import activate_user
from profiles.views import User
from referees.models import Referee


def create_and_activate_referee(data):
    if 'dob' in data:
        del data['dob']
    referee = Referee.objects.create_referee(**data)
    set_key(referee)
    activate_user(referee.user)
    return referee


def certify_referee(data):
    referee = create_and_activate_referee(data)
    referee.certified = True
    return referee


def create_and_activate_athlete(data):
    athlete = Athlete.objects.create_athlete(**data)
    set_key(athlete)
    activate_user(athlete.user)
    return athlete


def create_and_activate_both(data):
    both = Athlete.objects.create_athlete(**data)
    set_key(both)
    activate_user(both.user)
    both.user._referee = True
    return both


def create_and_activate_admin(data):
    user = User.objects.create_superuser(**data)
    set_key(user)
    activate_user(user)
    return user


def create_and_activate_staff(data):
    user = User.objects.create_staff(**data)
    set_key(user)
    activate_user(user)
    return user


def create_and_activate_user(data):
    user = User.objects.create_user(**data)
    set_key(user)
    activate_user(user)
    return user
