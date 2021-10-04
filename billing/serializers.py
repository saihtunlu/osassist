from rest_framework import serializers
from .models import Billing, BillingPayment, BillingImage, PaymentMethod
from membership_plan.serializers import MembershipPlanSerializers
from store.serializers import StoreSerializers


class PaymentMethodSerializers(serializers.ModelSerializer):

    class Meta:
        model = PaymentMethod
        fields = '__all__'


class BillingImageSerializers(serializers.ModelSerializer):

    class Meta:
        model = BillingImage
        fields = '__all__'


class BillingPaymentSerializers(serializers.ModelSerializer):
    images = BillingImageSerializers(many=True, read_only=True)
    payment_method = PaymentMethodSerializers(many=False, read_only=True)

    class Meta:
        model = BillingPayment
        fields = ['id', 'amount', 'date', 'images', 'payment_method']


class BillingSerializers(serializers.ModelSerializer):
    payments = BillingPaymentSerializers(many=True, read_only=True)
    selected_plan = MembershipPlanSerializers(many=False, read_only=True)

    store_name = serializers.CharField(
        source='store.name', read_only=True)

    class Meta:
        model = Billing
        fields = ['id', 'store', 'store_name', 'price', 'date', 'selected_plan', 'payments', 'note',
                  'total', 'status', 'payment_status', 'number_of_months']
