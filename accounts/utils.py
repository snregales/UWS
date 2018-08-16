from django.utils.text import slugify
from utils.utils import assert_slug_unique


def create_slug(**kwargs):
    """
    :return: a string who's components are first and last name,
     of the instance object, jointed together
    """
    return slugify(
        "{first} {last}".format(
            first=kwargs['first_name'],
            last=kwargs['last_name'],
        )
    )


def create_unique_slug(model, **kwargs):
    """
    :param model: object to traverse
    :return: a slug unique to the Profile model
    """
    if 'staff_alias' in kwargs:
        slug = 'staff-' + kwargs['staff_alias']
    elif 'admin_alias' in kwargs:
        slug = 'admin-' + kwargs['admin_alias']
    else:
        slug = create_slug(**kwargs)
    return assert_slug_unique(slug, model)
