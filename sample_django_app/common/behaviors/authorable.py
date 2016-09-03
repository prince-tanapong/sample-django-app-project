from django.db import models


class Authorable(models.Model):
    authored_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True
