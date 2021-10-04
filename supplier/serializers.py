from rest_framework import serializers
from .models import Supplier, BankAccountInformation


class BankAccountInformationSerializers(serializers.ModelSerializer):

    class Meta:
        model = BankAccountInformation
        fields = '__all__'


class SupplierSerializers(serializers.ModelSerializer):
    banks = BankAccountInformationSerializers(many=True, read_only=True)

    class Meta:
        model = Supplier
        fields = ['id', 'banks', 'store', 'name', 'facebook_page',
                  'contact_person', 'address', 'telephone', 'cp_mobile', 'cp_mail', 'created_at', 'updated_at', 'website']
