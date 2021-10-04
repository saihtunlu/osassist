from django.db import models
from django.conf import settings
from store.models import Store
User = settings.AUTH_USER_MODEL


class TrackableDateModel(models.Model):
    """Abstract model to Track the creation/updated date for a model."""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Supplier(TrackableDateModel):
    name = models.TextField(max_length=2000, null=True, blank=False)
    address = models.TextField(max_length=2000, blank=True, null=True)
    telephone = models.TextField(max_length=2000, blank=True, null=True)
    website = models.TextField(max_length=2000, blank=True, null=True)
    facebook_page = models.TextField(max_length=2000, blank=True, null=True)
    contact_person = models.TextField(max_length=2000, blank=True, null=True)
    cp_mobile = models.TextField(max_length=2000, blank=True, null=True)
    cp_mail = models.EmailField(
        max_length=2000, blank=True, unique=True, null=True)
    store = models.ForeignKey(Store, related_name='suppliers',
                              null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class BankAccountInformation(TrackableDateModel):
    supplier = models.ForeignKey(Supplier, related_name='banks',
                                 null=True, blank=True, on_delete=models.CASCADE)
    name = models.TextField(max_length=2000, null=True)
    account_number = models.TextField(max_length=2000, null=True)
    account_holder_name = models.TextField(max_length=2000, null=True)
