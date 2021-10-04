from django.db import models
from store.models import Store

class TrackableDateModel(models.Model):
    """Abstract model to Track the creation/updated date for a model."""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class FinanceLabel(TrackableDateModel):
    name = models.TextField(max_length=2000, null=True, default="", blank=True)
    store = models.ForeignKey(Store, related_name='finance_label',
                              null=True, blank=True, on_delete=models.CASCADE)

class Finance(TrackableDateModel):
    note = models.TextField(max_length=2000, null=True, default="", blank=True)
    date = models.TextField(max_length=2000, null=True, blank=True)
    type = models.TextField(max_length=2000, null=True, blank='Expense')
    amount = models.TextField(null=True, default=0)
    store = models.ForeignKey(Store, related_name='finances',
                              null=True, blank=True, on_delete=models.CASCADE)
    label = models.ForeignKey(FinanceLabel, related_name='label',
                              null=True, blank=True, on_delete=models.CASCADE)