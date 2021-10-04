from delivery.models import Delivery
from customer.models import Customer
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


class Sale(TrackableDateModel):
    sale_no = models.TextField(max_length=2000, null=True, unique=True)
    customer = models.ForeignKey(Customer, related_name='sales',
                                 null=True, blank=True, on_delete=models.CASCADE)
    subtotal = models.TextField(max_length=2000, null=True, default="0")
    money_price = models.TextField(max_length=2000, null=True, default="0")
    supplier_percentage = models.TextField(max_length=2000, null=True, default="5")
    phone = models.TextField(max_length=2000, null=True)
    total = models.IntegerField(null=True, default=0)
    discount = models.TextField(max_length=2000, null=True, default="0")
    paid_amount = models.TextField(max_length=2000, null=True, default="0")
    discount_reason = models.TextField(max_length=2000, null=True, blank=True)
    discount_type = models.TextField(max_length=2000, null=False, default='Ks')
    due_amount = models.TextField(max_length=2000, default='0', blank=True)
    payment_status = models.TextField(
        max_length=2000, default='Unpaid', blank=True)
    status = models.TextField(max_length=2000, null=True, default='Processing')
    note = models.TextField(max_length=2000, null=True, default="")
    date = models.TextField(null=True, blank=True, default="")
    is_fulfilled = models.BooleanField(default=False)
    delivery_company = models.ForeignKey(Delivery, related_name='sales',
                                         null=True, blank=True, on_delete=models.SET_NULL)
    store = models.ForeignKey(Store, related_name='sales',
                              null=True, blank=True, on_delete=models.CASCADE)

class SaleProduct(TrackableDateModel):
    sale = models.ForeignKey(Sale, related_name='products',
                             null=True, blank=True, on_delete=models.CASCADE)
    quantity = models.TextField(max_length=2000, null=True, default="0")
    number_of_fullfilled = models.TextField(
        max_length=2000, null=True, default="0")
    primary_price = models.TextField(max_length=2000, null=True, default="0")
    primary_price_myanmar = models.TextField(
        max_length=2000, null=True, default="0")
    sale_price = models.TextField(max_length=2000, null=True, default="0")
    subtotal = models.TextField(max_length=2000, null=True, default="0")
    margin = models.TextField(max_length=2000, null=True, default="0")
    profit = models.TextField(max_length=2000, null=True, default="0")
    name = models.TextField(max_length=2000, null=True, blank=True)
    image = models.TextField(max_length=2000, null=True, blank=True)
    link = models.TextField(max_length=2000, null=True, blank=True)
    date = models.TextField(max_length=2000, null=True, blank=True)
    store = models.ForeignKey(Store, related_name='sale_products',
                              null=True, blank=True, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.name)


class SalePayment(TrackableDateModel):
    sale = models.ForeignKey(Sale, related_name='payments',
                             null=True, blank=True, on_delete=models.CASCADE)
    amount = models.TextField(max_length=2000, default='0', blank=True)
    date = models.TextField(max_length=2000, default='0', blank=True)
    store = models.ForeignKey(Store, related_name='sale_payments',
                              null=True, blank=True, on_delete=models.CASCADE)

class SaleAddress(TrackableDateModel):
    sale = models.OneToOneField(
        Sale,
        related_name='address',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    address = models.TextField(max_length=2000,  blank=True, null=True)
    state = models.TextField(max_length=2000, blank=True, null=True)
    city = models.TextField(max_length=2000, blank=True, null=True)
