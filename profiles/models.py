from django.conf import settings
from django.db import models

from .utils import create_unique_id

User = settings.AUTH_USER_MODEL


class ProfileQuerySet(models.QuerySet):
    def get_user_instance_id(self, _id):
        profile = self.filter(id__exact=_id)
        if profile.exists():
            return profile.first()
        return None

    def get_user_instance_email(self, email):
        profile = self.filter(user_id__exact=email)
        if profile.exists() and profile.count() is 1:
            return profile.first()
        return None


class ProfileManager(models.Manager):
    def get_queryset(self):
        return ProfileQuerySet(self.model, using=self._db)

    def get_user_key(self, email):
        profile = self.get_queryset().get_user_instance_email(email)
        if profile:
            return profile.user.key
        return None

    def get_user_fullname(self, email):
        profile = self.get_queryset().get_user_instance_email(email)
        if profile:
            return profile.__str__
        return None


class Profile(models.Model):
    id = models.CharField(max_length=19, primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255, verbose_name='First Name')
    last_name = models.CharField(max_length=255, verbose_name='Last Name')
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = ProfileManager()

    class Meta:
        abstract = True

    @property
    def __str__(self):
        return self.fullname

    @property
    def fullname(self):
        return "{first} {last}".format(
            first=self.first_name,
            last=self.last_name
        )

    @property
    def slug(self):
        return self.user.slug


def pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.id:
        instance.id = create_unique_id(instance)
