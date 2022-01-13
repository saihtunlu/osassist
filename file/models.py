from django.db import models

# Create your models here.
from django.db import models
from store.models import Store

class TrackableDateModel(models.Model):
    """Abstract model to Track the creation/updated date for a model."""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class File(TrackableDateModel):
    image = models.TextField(null=False,blank=False)
    store = models.ForeignKey(Store, related_name='files',
                              null=True, blank=True, on_delete=models.CASCADE)
  