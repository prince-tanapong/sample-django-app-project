from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Authorable(models.Model):
    author = models.ForeignKey(User)

    class Meta:
        abstract = True


class Permalinkable(models.Model):
    slug = models.SlugField()

    class Meta:
        abstract = True


class Publishable(models.Model):
    publish_date = models.DateTimeField(null=True)

    class Meta:
        abstract = True

    def publish_on(self, date=None):
        if not date:
            date = timezone.now()
        self.publish_date = date
        self.save()

    @property
    def is_published(self):
        return self.publish_date and self.publish_date < timezone.now()


class Timestampable(models.Model):
    create_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
