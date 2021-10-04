from rest_framework import serializers
from .models import Sale, SaleProduct, SalePayment,SaleAddress
from customer.serializers import CustomerSerializers

class SaleAddressSerializers(serializers.ModelSerializer):

    class Meta:
        model = SaleAddress
        fields = ["address", "city", "state"]


class SaleProductSerializers(serializers.ModelSerializer):
    customer_name = serializers.CharField(
        source='sale.customer.name', read_only=True)
    class Meta:
        model = SaleProduct
        fields = ['id', 'sale','customer_name', 'primary_price', 'date', 'margin', 'profit', 'quantity', 'number_of_fullfilled', 'primary_price_myanmar', 'sale_price',
                  'subtotal',  'name', 'link', 'image','store', 'created_at']


class SalePaymentSerializers(serializers.ModelSerializer):
    class Meta:
        model = SalePayment
        fields = "__all__"


class SaleSerializers(serializers.ModelSerializer):
    address = SaleAddressSerializers(many=False, read_only=True)
    products = SaleProductSerializers(many=True, read_only=True)
    customer = CustomerSerializers(many=False, read_only=True)
    payments = SalePaymentSerializers(many=True, read_only=True)
    customer_name = serializers.CharField(
        source='customer.name', read_only=True)
    delivery_company_name=serializers.CharField(
        source='delivery_company.name', read_only=True)
    class Meta:
        model = Sale
        fields = ['id',
                  'date',
                  'address',
                  'money_price',
                  'supplier_percentage',
                  'is_fulfilled',
                  'paid_amount',
                  'note',
                  'customer',
                  "customer_name",
                  "phone",
                  'products',
                  'sale_no',
                  "subtotal",
                  "total",
                  "payments",
                  'payment_status',
                  'status',
                  "discount",
                  "due_amount",
                  "discount_reason",
                  "discount_type",
                  'paid_amount',
                  'created_at',
                  'delivery_company_name',
                  'updated_at']


class SaleListSerializers(serializers.ModelSerializer):
    customer_name = serializers.CharField(
        source='customer.name', read_only=True)
    products = SaleProductSerializers(many=True, read_only=True)
    class Meta:
        model = Sale
        fields = ['id',
                  'date',
                  'is_fulfilled',
                  'products',
                  "customer_name",
                  'sale_no',
                  "total",
                  'payment_status',
                  'paid_amount',
                  'updated_at',
                  'created_at']

