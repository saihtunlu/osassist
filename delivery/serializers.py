from rest_framework import serializers
from .models import Delivery


class DeliverySerializers(serializers.ModelSerializer):

    class Meta:
        model = Delivery
        fields = ['id',  'name',
                  'contact_person', 'address', 'telephone', 'store', 'cp_mobile', 'priority', 'created_at', 'updated_at', 'Remark',]
