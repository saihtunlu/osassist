from store.models import Store
from django.db import models
from django.conf import settings
User = settings.AUTH_USER_MODEL


class TrackableDateModel(models.Model):
    """Abstract model to Track the creation/updated date for a model."""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Delivery(TrackableDateModel):
    name = models.TextField(max_length=2000, null=True, unique=True)
    address = models.TextField(max_length=2000, blank=True, null=True)
    telephone = models.TextField(max_length=2000, blank=True, null=True)
    contact_person = models.TextField(max_length=2000, blank=True, null=True)
    cp_mobile = models.TextField(max_length=2000, blank=True, null=True)
    priority = models.TextField(max_length=2000, blank=True, null=True)
    Remark = models.TextField(max_length=2000, blank=True, null=True)
    store = models.ForeignKey(Store, related_name='deliveries',
                              null=True, blank=True, on_delete=models.CASCADE)

    def __unicode__(self):
        return self.name
