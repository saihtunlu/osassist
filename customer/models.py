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


class Customer(TrackableDateModel):
    name = models.TextField(max_length=2000, null=True)
    email = models.EmailField(max_length=2000, null=True, unique=True)
    note = models.TextField(max_length=2000, blank=True, null=True)
    phone = models.TextField(max_length=2000, blank=True, null=True)
    store = models.ForeignKey(Store, related_name='customers',
                              null=True, blank=True, on_delete=models.CASCADE)

    def __unicode__(self):
        return self.name


class CustomerAddress(TrackableDateModel):
    customer = models.OneToOneField(
        Customer,
        related_name='address',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    address = models.TextField(max_length=2000,  blank=True, null=True)
    state = models.TextField(max_length=2000, blank=True, null=True)
    city = models.TextField(max_length=2000, blank=True, null=True)
