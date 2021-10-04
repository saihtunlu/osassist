from store.models import Store
from membership_plan.models import MembershipPlan
from django.db import models

# Create your models here.
from django.db import models


class TrackableDateModel(models.Model):
    """Abstract model to Track the creation/updated date for a model."""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class PaymentMethod(TrackableDateModel):
    name = models.TextField(max_length=2000, default='0', blank=True)
    payment_number = models.TextField(max_length=2000, default='0', blank=True)


class Billing(TrackableDateModel):
    selected_plan = models.ForeignKey(MembershipPlan, related_name='store_billings',
                                      null=True, blank=True, on_delete=models.CASCADE)

    store = models.ForeignKey(
        Store,
        related_name='billings',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    total = models.TextField(max_length=2000, default='0', blank=True)
    date = models.TextField(max_length=2000, default='0', blank=True)
    price = models.TextField(max_length=2000, default='0', blank=True)
    number_of_months = models.TextField(
        max_length=2000, default='0', blank=True)
    note = models.TextField(max_length=2000, default='', blank=True)
    status = models.TextField(
        max_length=2000, null=True,  default='Pending')
    payment_status = models.TextField(
        max_length=2000, null=True,  default='Unpaid')


class BillingPayment(TrackableDateModel):
    billing = models.ForeignKey(Billing, related_name='payments',
                                null=True, blank=True, on_delete=models.CASCADE)
    amount = models.TextField(max_length=2000, default='0', blank=True)
    date = models.TextField(max_length=2000, default='0', blank=True)
    payment_method = models.ForeignKey(PaymentMethod, related_name='method_billings',
                                       null=True, blank=True, on_delete=models.CASCADE)


class BillingImage(TrackableDateModel):
    image = models.TextField(
        max_length=2000,  default='/media/default.png', null=True)
    billing_payment = models.ForeignKey(BillingPayment, related_name='images',
                                        null=True, blank=True, on_delete=models.CASCADE)
