from django.db import models

# Create your models here.
from django.db import models


class TrackableDateModel(models.Model):
    """Abstract model to Track the creation/updated date for a model."""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class MembershipPlan(TrackableDateModel):
    price = models.TextField(
        max_length=2000, null=True, default='')
    name = models.TextField(max_length=2000, null=True,  default='Basic')
    description = models.TextField(max_length=2000, null=True,  default='')
    features=models.TextField(null=True,  default='')
    def __str__(self):
        return self.name

