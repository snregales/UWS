from django.db.models.signals import pre_save

from profiles.models import (
    pre_save_receiver,
    Profile,
    ProfileManager,
    models,
)


class AthleteManager(ProfileManager):
    def create_athlete(self, **kwargs):
        from accounts.models import User
        kwargs.update({
            'user': User.objects.create_athlete(**kwargs['user'])
        })
        return self.create(
            **kwargs
        )


class Athlete(Profile):
    dob = models.DateField(blank=True, null=True, verbose_name='Date of Birth')
    objects = AthleteManager()

    class Meta:
        db_tablespace = "athlete_indexes"
        ordering = ['last_name', 'first_name']
        indexes = [
            models.Index(name='last_modified', fields=['-updated', 'timestamp']),
            models.Index(name='age_ordering', fields=['-dob'])
        ]


pre_save.connect(receiver=pre_save_receiver, sender=Athlete)
