from supplier.models import Supplier
from django.db import models
from store.models import Store
from sale.models import Sale

class TrackableDateModel(models.Model):
    """Abstract model to Track the creation/updated date for a model."""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Order(TrackableDateModel):
    note = models.TextField(max_length=2000, null=True, default="", blank=True)
    date = models.TextField(max_length=2000, null=True, blank=True)
    total = models.TextField(null=True, default=0)
    store = models.ForeignKey(Store, related_name='orders',
                              null=True, blank=True, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, related_name='orders',
                                 null=True, blank=True, on_delete=models.SET_NULL)

class OrderProduct(TrackableDateModel):
    order = models.ForeignKey(Order, related_name='products',
                              null=True, blank=True, on_delete=models.CASCADE)
    sale = models.ForeignKey(Sale, related_name='order_product',
                              null=True, blank=True, on_delete=models.CASCADE)
    quantity = models.TextField(max_length=2000, null=True, default="0")
    price = models.TextField(max_length=2000, null=True, default="0")
    subtotal = models.TextField(max_length=2000, null=True, default="0")
    name = models.TextField(max_length=2000, null=True, blank=True)
    image = models.TextField(max_length=2000, null=True, blank=True)
    link = models.TextField(max_length=2000, null=True, blank=True)
    link = models.TextField(max_length=2000, null=True, blank=True)
    