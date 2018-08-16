from django import forms
from django.contrib.auth import get_user_model
from pyisemail import is_email

User = get_user_model()


def validate_email(email):
    """
    uses the pyisemail API to validate if email is legitimate
    pyisemail API needs a proper internet connection
    :param email: str
    :return: email if passed
    """
    # if not is_email(email, check_dns=True):
    #     raise forms.ValidationError("Email is not legit")
    return email


def validate_password(initial, confirm):
    if initial and confirm and initial != confirm:
        raise forms.ValidationError("Passwords don't match")
    if initial.__len__() < 8:
        raise forms.ValidationError("Password is to short")
    return initial


def validate_email_absence(email):
    if not email:
        raise forms.ValidationError("Email Field must be filled")
    if User.objects.filter(email__exact=email).exists():
        raise forms.ValidationError("Email already registered")
    return email


def validate_email_exists(email):
    if not email:
        raise forms.ValidationError("Email Field must be filled")
    if not User.objects.filter(email__exact=email).exists():
        raise forms.ValidationError("Not found")
    return email


def validate_participants(slug, team):
    from events.models import Event
    meta = Event.objects.get_queryset().get_event_instance_slug(slug).eventmeta
    if len(meta.teams.all()) > 16:
        raise forms.ValidationError('Event participants quota already met')
    for t in meta.teams.all():
        if team.name == t.name:
            raise forms.ValidationError('Team already registered to event')
    return team


def validate_event_name(name, model):
    obj = model.objects.filter(name__iexact=name)
    if obj.exists():
        raise forms.ValidationError('Event already exists')
    return name


def validate_date(date):
    from .utils import get_utc_timestamp
    from datetime import timedelta
    allowed = get_utc_timestamp().date() + timedelta(weeks=2)
    if date.date() < allowed:
        raise forms.ValidationError(
            'Date must be at least on {} or later'.format(allowed.strftime('%d %B %Y'))
        )
    return date
