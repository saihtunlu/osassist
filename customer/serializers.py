from rest_framework import serializers
from .models import Customer, CustomerAddress


class CustomerAddressSerializers(serializers.ModelSerializer):

    class Meta:
        model = CustomerAddress
        fields = ["address", "city",  "state"]



class CustomerSerializers(serializers.ModelSerializer):
    address = CustomerAddressSerializers(
        many=False, read_only=True)
  

    class Meta:
        model = Customer
        fields = ['id', 'name',
                  'email', 'phone',  'address', 'note', 'sales', 'store', 'created_at', 'updated_at']
