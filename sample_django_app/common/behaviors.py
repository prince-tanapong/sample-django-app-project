from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from django.utils.timezone import now


class Annotatable(models.Model):
    notes = models.ManyToManyField('common.Note')

    class Meta:
        abstract = True

    @property
    def has_notes(self):
        return True if self.notes.count() else False


class Authorable(models.Model):

    authored_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True


class Expirable(models.Model):
    valid_at = models.DateTimeField(null=True, blank=True)
    expired_at = models.DateTimeField(null=True, blank=True)

    @property
    def is_expired(self):
        return True if self.expired_at and self.expired_at < now() else False

    class Meta:
        abstract = True


class Locatable(models.Model):
    longitude = models.FloatField(null=True)
    latitude = models.FloatField(null=True)

    class Meta:
        abstract = True


class Permalinkable(models.Model):
    slug = models.SlugField(null=True, blank=True)

    class Meta:
        abstract = True

    def get_url_kwargs(self, **kwargs):
        kwargs.update(getattr(self, 'url_kwargs', {}))
        return kwargs

    @models.permalink
    def get_absolute_url(self):
        url_kwargs = self.get_url_kwargs(slug=self.slug)
        return (self.url_name, (), url_kwargs)


@receiver(pre_save, sender=Permalinkable)
def pre_save(self, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(self.slug_source)


class Timestampable(models.Model):
    create_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
