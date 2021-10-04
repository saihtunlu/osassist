from rest_framework import serializers
from .models import FinanceLabel,Finance


class FinanceLabelSerializers(serializers.ModelSerializer):

    class Meta:
        model = FinanceLabel
        fields = "__all__"

class FinanceSerializers(serializers.ModelSerializer):
    label = FinanceLabelSerializers(many=False, read_only=True)
    store_name = serializers.CharField(
        source='store.name', read_only=True)
    balance = serializers.CharField(
        source='store.balance', read_only=True)
    label_name = serializers.CharField(
        source='label.name', read_only=True)
    class Meta:
        model = Finance
        fields = ['id',  'note','label','label_name','store_name','store','balance',
                  'date', 'amount', 'type','created_at', 'updated_at']
