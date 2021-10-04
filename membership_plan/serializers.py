from rest_framework import serializers
from .models import MembershipPlan




class MembershipPlanSerializers(serializers.ModelSerializer):

    class Meta:
        model = MembershipPlan
        fields = ['id', 'name', 'price',
           'description', 'created_at','features', 'updated_at']
