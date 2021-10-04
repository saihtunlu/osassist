from rest_framework import serializers
from .models import Store,  Plan
from membership_plan.serializers import MembershipPlanSerializers


class PlanSerializers(serializers.ModelSerializer):

    plan = MembershipPlanSerializers(many=False, read_only=True)

    class Meta:
        model = Plan
        fields = ['id', 'store', 'plan',
                  'free_trail_exp_date', 'exp_date', 'status', 'updated_at']

class StoreSerializers(serializers.ModelSerializer):
    plan = PlanSerializers(many=False, read_only=True)
    class Meta:
        model = Store
        fields = ['id', 'name',  'primary_color', 'currency','address'
                  ,'email', 'phone','balance', 'fbLink',  'logo',   'created_at', 'updated_at','plan']
