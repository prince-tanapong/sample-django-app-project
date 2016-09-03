from django.db import models
from django.utils import timezone

from .behaviors import (
    Authorable,
    Permalinkable,
    Publishable,
    Timestampable
)


class BlogPostManager(models.Manager):

    def published(self):
        return self.filter(publish_date__lte=timezone.now())

    def authored_by(self, author):
        return self.filter(author__username=author)


class BlogPost(
    Authorable, Permalinkable, Timestampable, Publishable, models.Model
):
    title = models.CharField(max_length=255)
    body = models.TextField()

    objects = BlogPostManager()
