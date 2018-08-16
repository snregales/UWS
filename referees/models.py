from django.db.models.signals import pre_save
from profiles.models import (
    pre_save_receiver,
    Profile,
    ProfileManager,
    models,
)


class RefereeManager(ProfileManager):
    def create_referee(self, **kwargs):
        from accounts.models import User
        kwargs.update({
            'user': User.objects.create_referee(**kwargs['user'])
        })
        return self.create(
            **kwargs
        )


class Referee(Profile):
    certified = models.BooleanField(default=False)
    objects = RefereeManager()

    class Meta:
        db_tablespace = "referee_indexes"
        ordering = ['last_name', 'first_name']
        indexes = [
            models.Index(name='last_modified', fields=['-updated', 'timestamp']),
        ]


pre_save.connect(receiver=pre_save_receiver, sender=Referee)
