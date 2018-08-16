import random
import string
from datetime import datetime
from pytz import timezone, reference

from django.conf import settings
from django.urls import reverse
from django.utils.encoding import force_text as _
from django.template.loader import render_to_string

SHORTCODE_MIN = getattr(settings, "SHORTCODE_MIN", 32)
DONT_SLUG = ['admin', 'athlete', 'referee', 'exam', 'usr',
             'util', 'login', 'logout', 'register',
             ]


def random_string_generator(size=SHORTCODE_MIN, chars=string.ascii_uppercase + string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def get_timestamp():
    return datetime.now(reference.LocalTimezone()).replace(microsecond=0)


def get_utc_timestamp():
    return datetime.now(reference.UTC).replace(microsecond=0)


def choice_list(model):
    """
    takes in a model iterate through the model and creates a list from its elements
    :note: model must have field id
    :param model: whatever model you want to create a list from
    :return: return a tuple list of elements in the model (element_id, element_name)
    """
    return [(e.id, e.__str__) for e in model.objects.all()]


def append_to_slug(slug):
    """
    append to the back of the slug with a underscore between
    :param slug: is a string
    :return: modified slug
    """
    return "{slug}_{randchar}".format(
            slug=slug,
            randchar=random_string_generator(size=1, chars=string.digits))


def assert_slug_unique(slug, model):
    """
    check if the incoming slug is unique,
    if not, recursively add characters to it until it is
    :param model: object to search slug on
    :param slug: is a string
    :return: unique slug
    """
    if slug in DONT_SLUG:
        return assert_slug_unique(append_to_slug(slug), model)
    if model.objects.filter(slug__exact=slug).exists():
        return assert_slug_unique(append_to_slug(slug), model)
    return slug


# might need to re-evaluate this def, it should be in the accounts.models User class

def set_key(instance, key=None):
    """
    if key set instance's key to key
    else set instance's key to a random str
    :param key: str
    :param instance: is an Profile instance
    :return: instance's key
    """
    if key:
        instance.key = key
    else:
        instance.key = random_string_generator()
    instance.key_date = datetime.now(timezone('UTC')).replace(microsecond=0)
    instance.save()
    return instance.key


def is_key_valid(instance, key):
    if not key:
        raise ValueError('key cannot be empty')
    if not (instance.key and instance.key == key):
        return False
    date_delta = datetime.now(timezone('UTC')).replace(microsecond=0) - instance.key_date
    if date_delta.days >= settings.PASSWORD_RESET_TIMEOUT_DAYS:
        return False
    return True


def assert_id_unique(rfid, now):
    """
    takes an newly created rfid and check if it already exists on the database
    if true call create_unique_referee_id with the same current time
    :param rfid: id string composed of uppercase ascii char and positive integer
    :param now: Datetime
    :return: unique RFID
    """
    from referees.models import Referee
    from athletes.models import Athlete

    if Referee.objects.filter(id__exact=rfid).exists() or Athlete.objects.filter(id__exact=rfid).exists():
        return create_id(now)
    return rfid


def create_id(now):
    """
    Pulls the current date and compose it with some random letter to create a Referee ID (RFID)
    than delegate the id and time to assert_referee_id to assure id uniqueness
    :type now: datetime.now
    :return: unique RFID
    """
    return '{head}{now}{tail}'.format(
        head=random_string_generator(size=2, chars=string.ascii_uppercase),
        now=str(now).upper(),
        tail=random_string_generator(size=2, chars=string.ascii_uppercase)
    )


def password_change_prep(instance):
    if instance.is_active:
        # TODO: encrypt 'password change'
        set_key(instance, 'Forgot Password')
    return instance


def send_request_email(instance):
    domain = settings.DOMAIN + reverse(
        'pass change prep',
        kwargs={
            "slug": _(instance.slug),
            "code": _(set_key(instance))
        }
    )
    name = ''
    if instance.is_athlete:
        name = instance.athlete.__str__
    elif instance.is_referee:
        name = instance.referee.__str__
    elif 'admin' or 'staff' in instance.slug:
        name = instance.slug[6:]
        name = name[0].upper() + name[1:]
    context = {'name': name, 'domain': domain}
    plain = render_to_string('registration/password_change_request_email.html', context)
    print(plain)
    # return send_mail(
    #     subject='Password Reset Request',
    #     message=plain,
    #     from_email=settings.DEFAULT_FROM_EMAIL,
    #     recipient_list=[email],
    #     fail_silently=True
    # )
