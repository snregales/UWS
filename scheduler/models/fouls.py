from djongo import models


class Foul(models.Model):
    code = models.SlugField(max_length=2, primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(blank=True, null=True)
    objects = models.DjongoManager()

    def __str__(self):
        return self.name
