from datetime import datetime
from django.core.mail import (
    send_mail,
    settings,
)
from django.urls import reverse
from utils.utils import (
    assert_id_unique,
    create_id,
    set_key,
)


def create_unique_id(instance, now=None):
    """
    pk should be as follow %R%RD%HH%d%b%yM%MT%R%R,
    where %R is a random uppercase ascii letter
    %H is military hours %M minutes
    %d days %b uppercase 3 letter month code %y 2 digit year
    :param instance: a Profile instance (Referee, Athlete)
    :param now: datetime.now() tmzn = 'UTC'
    :return: return a unique id with timestamp component
    """
    if not now:
        now = datetime.now().strftime('D%HH%d%b%yM%MT')
    return assert_id_unique(
        create_id(now),
        now,
    )


def activate_user(instance):
    """
    check if user is activated, if not activate him/her
    and set his/her key to null
    :param instance: is a User instance
    :return: instance
    """
    if not instance.is_active:
        instance.active = True
        instance.key = None
        instance.save()
    return instance


def send_activation_email(instance):
    """
    send an email to the user to prompt him/her to activate account
    :param instance: a user
    :return: return an email
    """
    if not instance.is_active:
        full_path = "localhost:8000" + reverse('activate', kwargs={"code": set_key(instance)})
        print(full_path)
        print("email to ", str(instance.__str__))
        # return full_path
        return send_mail(
            'Activate Account',
            'Activate your account here: {}'.format(full_path),
            'sharlonregales@gmail.com',
            # str(settings.DEFAULT_FROM_EMAIL),
            ['sharlonregales+dev@gmail.com'],
        )


def prep_dict(**kwargs):
    kwargs.update({
        'user': {
            'email': kwargs['email'],
            'first_name': kwargs['first_name'],
            'last_name': kwargs['last_name'],
            'password': kwargs['initial'],
        }
    })
    del kwargs['email']
    del kwargs['initial']
    del kwargs['confirm']
    return kwargs
