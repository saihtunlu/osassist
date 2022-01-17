from rest_framework import serializers
from .models import Order


class OrderSerializers(serializers.ModelSerializer):
    store_name = serializers.CharField(
        source='store.name', read_only=True)
    cargo_name = serializers.CharField(
        source='cargo.name', read_only=True)
    class Meta:
        model = Order
        fields = ['id',
                  'code',
                  'app',
                  'status',
                  'store_name',
                  'cargo_name',
                  'created_at',
                  'updated_at', ] 
