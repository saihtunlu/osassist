from django.contrib.auth.models import update_last_login
import django.contrib.auth.password_validation as validators
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User
from rest_framework import serializers
from store.serializers import StoreSerializers


class UserSerializer(serializers.ModelSerializer):

    store = StoreSerializers(many=False, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'is_superuser', 'first_name',
                  'last_name', 'email', 'avatar', 'username', 'role', 'is_staff', 'is_active', 'last_login', 'date_joined',  'store']


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=255, required=True)
    password = serializers.CharField(
        max_length=255, required=True, write_only=True, validators=[validators.validate_password])
    password_confirm = serializers.CharField(
        max_length=255, required=True, write_only=True)

    def validate(self, data):
        if data['password'] != data['password_confirm']:  # both return None
            raise serializers.ValidationError(
                {'message': ["Your password and confirmation password do not match."]})

        return data

    def validate_old_password(self, value):
        if not self.context['user'].check_password(value):  # got data
            raise serializers.ValidationError("Incorrect Old Password")

        return value

    def update(self, instance, validated_data):

        instance.set_password(validated_data['password'])
        instance.save()

        return instance


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        data['is_superuser'] = self.user.is_superuser
        update_last_login(None, self.user)
        return data
