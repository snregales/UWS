"""
main point of recreating the account model, instead of using the one provided by django.
Is so we can customize it to our needs. We will divert the need of a username to the
the use of email to login. we will also remove the use of __groups in the system.
"""
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
)
from .utils import create_unique_slug


class UserManager(BaseUserManager):
    def create_user(self, **kwargs):
        if not ('email' in kwargs and kwargs['email']):
            raise ValueError("User_model must have a email")
        if not ('password' in kwargs and kwargs['password']):
            raise ValueError("User_model must have a password")
        user = self.model(
            email=self.normalize_email(kwargs['email'])
        )
        user.set_password(kwargs['password'])
        user.set_slug(create_unique_slug(User, **kwargs))
        user.save(using=self._db)
        return user

    def create_staff(self, **kwargs):
        user = self.create_user(**kwargs)
        user.staff = True
        user.save()
        return user

    def create_superuser(self, **kwargs):
        user = self.create_user(**kwargs)
        user.staff = True
        user.admin = True
        user.active = True
        user.save()
        return user

    def create_athlete(self, **kwargs):
        user = self.create_user(**kwargs)
        user._athlete = True
        user.save()
        return user

    def create_referee(self, **kwargs):
        user = self.create_user(**kwargs)
        user._referee = True
        user.save()
        return user

    def get_user_instance_slug(self, slug):
        profile = self.filter(slug__exact=slug)
        if profile.exists():
            return profile.first()
        return None


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='Email',
        max_length=225,
        primary_key=True)
    key = models.CharField(max_length=20, blank=True, null=True)
    key_date = models.DateTimeField()
    slug = models.SlugField()
    active = models.BooleanField(default=False)
    staff = models.BooleanField(default=False)
    _referee = models.BooleanField(default=False)
    _athlete = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    @property
    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the account have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the account have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_referee(self):
        return self._referee

    @property
    def is_athlete(self):
        return self._athlete

    @property
    def is_ref_and_athlete(self):
        return self.is_referee and self.is_athlete

    @property
    def is_active(self):
        return self.active

    @property
    def is_admin(self):
        return self.admin

    def set_slug(self, slug):
        if not self.slug:
            self.slug = slug
