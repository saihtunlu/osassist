from django.db import models
from membership_plan.models import MembershipPlan
# Create your models here.


class TrackableDateModel(models.Model):
    """Abstract model to Track the creation/updated date for a model."""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Store(TrackableDateModel):
    name = models.TextField(max_length=2000, null=True)
    email = models.EmailField(
        max_length=2000, null=True, blank=True, unique=True)
    logo = models.TextField(max_length=2000, null=True,
                            default='/media/default.png')
    phone = models.TextField(max_length=2000, null=True, blank=True)
    fbLink = models.TextField(max_length=2000, null=True, blank=True)
    type = models.TextField(max_length=2000, null=True, blank=True)
    status = models.TextField(
        max_length=2000, null=True,  default='Active')
    primary_color = models.TextField(
        max_length=2000, null=True, default='#a177f7')
    currency = models.TextField(max_length=2000, null=True,  default='MMK')
    address = models.TextField(max_length=2000, null=True,  default='')
    balance = models.TextField(max_length=2000, null=True,  default='0')

    def __str__(self):
        return self.name + ' - ' + self.email

class Plan(TrackableDateModel):
    store = models.OneToOneField(
        Store,
        related_name='plan',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    plan = models.ForeignKey(
        MembershipPlan,
        related_name='store',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    status = models.TextField(
        max_length=2000, null=True,  default='Active')
    exp_date = models.DateTimeField(null=True)
    free_trail_exp_date = models.DateTimeField(null=True)