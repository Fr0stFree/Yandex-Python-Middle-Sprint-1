import uuid

from django.db import models


class TimeStampedMixin(models.Model):
    class Meta:
        abstract = True

    modified = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)


class UUIDMixin(models.Model):
    class Meta:
        abstract = True

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
