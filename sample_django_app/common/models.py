import uuid

from django.contrib.postgres.fields import JSONField
from django.db import models

from .behaviors import (
    Authorable,
    Timestampable
)


class Currency(Timestampable, models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=3)

    def __unicode__(self):
        return self.code


class Country(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, blank=True)
    code = models.CharField(max_length=3, blank=True)
    calling_code = models.CharField(max_length=3, blank=True)
    currency = models.ForeignKey(
        Currency, related_name='countries', null=True
    )

    def __unicode__(self):
        return self.code

    class Meta:
        verbose_name_plural = 'countries'


class Address(Timestampable, models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    line_1 = models.CharField(max_length=100, null=True, blank=True)
    line_2 = models.CharField(max_length=100, null=True, blank=True)
    line_3 = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=35, null=True, blank=True)
    region = models.CharField(max_length=35, null=True, blank=True)
    postal_code = models.CharField(max_length=10, null=True, blank=True)
    country = models.ForeignKey(
        'common.Country', related_name='addresses', null=True
    )

    @property
    def inline_string(self):
        string = "%s " % self.line_1
        string += "%s" % self.city or ""
        string += ", %s " % self.region or ""
        return string

    @property
    def google_map_url(self):
        return "http://maps.google.com/?q=%s" % self.inline_string.replace(
            " ", "%20"
        )

    def __unicode__(self):
        return unicode(self.inline_string)

    class Meta:
        verbose_name_plural = 'addresses'


class Note(Timestampable, Authorable, models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    text = models.TextField(default="", blank=True)


class Upload(Timestampable, models.Model):
    original = models.URLField(default="")
    name = models.CharField(max_length=50, blank=True, null=True)
    thumbnail = models.URLField(default="", blank=True, null=True)
    meta_data = JSONField(blank=True, null=True)

    @property
    def file_type(self):
        return self.meta_data.get('type', "") if self.meta_data else ""

    @property
    def is_image(self):
        return True if 'image' in self.file_type else False

    @property
    def is_pdf(self):
        return True if 'pdf' in self.file_type else False

    @property
    def width(self):
        if self.is_image:
            return self.meta_data['meta'].get(
                'width') if self.meta_data.get('meta') else None

    @property
    def height(self):
        if self.is_image:
            return self.meta_data['meta'].get(
                'height') if self.meta_data.get('meta') else None

    @property
    def file_extension(self):
        return self.meta_data.get('ext', "")

    @property
    def link_title(self):
        if self.name:
            title = self.name
        elif 'etc' in self.meta_data:
            title = (self.meta_data['etc'] or "").upper()
        else:
            title = (self.meta_data['type'] or "").upper(
                ) if 'type' in self.meta_data else ""
        if 'ext' in self.meta_data:
            title = title + " .%s" % (self.meta_data['ext'] or "").upper()
        return title
