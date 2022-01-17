from django.db import models
from store.models import Store
from supplier.models import Supplier

class TrackableDateModel(models.Model):
    """Abstract model to Track the creation/updated date for a model."""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Order(TrackableDateModel):
    code = models.TextField(max_length=2000, null=True, blank=True)
    status = models.TextField(max_length=2000, null=True, blank=True)
    app = models.TextField(max_length=2000, null=True, blank=True)
    store = models.ForeignKey(Store, related_name='orders',
                              null=True, blank=True, on_delete=models.CASCADE)
    cargo = models.ForeignKey(Supplier, related_name='orders',
                                 null=True, blank=True, on_delete=models.CASCADE)