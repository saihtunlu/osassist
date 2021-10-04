from rest_framework import serializers
from .models import Order, OrderProduct


class OrderProductSerializers(serializers.ModelSerializer):
    customer_name = serializers.CharField(
            source='sale.customer.name', read_only=True)
    class Meta:
        model = OrderProduct
        fields = [
            'id', 'order', 'quantity','price','sale','customer_name',
                  'subtotal',  'name', 'link', 'image', 'created_at']


class OrderSerializers(serializers.ModelSerializer):
    products = OrderProductSerializers(many=True, read_only=True)
    supplier_name = serializers.CharField(
        source='supplier.name', read_only=True)
    store_name = serializers.CharField(
        source='store.name', read_only=True)
    class Meta:
        model = Order
        fields = ['id',
                  'date',
                  'products',
                  'note',
                  'supplier',
                  'supplier_name',
                  'total',
                  'created_at',
                  'store_name',
                  'updated_at', ] 
