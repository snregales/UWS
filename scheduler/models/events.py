from djongo import models
from events.models import Event
from .groups import Group


class FixedEvent(models.Model):
    """
    This model holds all events that are already been scheduled
    and has OneToOneField event that is connected to Event Model Class
    and holds two ArrayReferenceField Group and Playoff
    """
    event = models.OneToOneField(
        to=Event,
        on_delete=models.CASCADE
    )
    groups = models.ArrayReferenceField(
        to=Group,
        on_delete=models.CASCADE,
    )
    objects = models.DjongoManager()

    def __str__(self):
        return self.event.__str__()

    @property
    def slug(self):
        """
        :return: the event slug
        """
        return self.event.slug

    @property
    def get_groups(self):
        """
        :return: list object of __groups
        """
        return self.groups

    def add_to_group(self, groups):
        """
        add group to __groups
        :param groups: Group object
        :return: __groups, ArrayReferenceField
        """
        if not isinstance(groups, list):
            raise AttributeError('{} is not a {} object/instance'.format(groups, list))
        for group in groups:
            if not isinstance(group, Group):
                raise AttributeError('{} is not a {} object/instance'.format(groups, Group))
        return self.groups.add(*groups)
