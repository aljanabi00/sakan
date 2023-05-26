from rest_framework import serializers
from .models import *


class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Package
        fields = '__all__'


class AccountTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountType
        fields = '__all__'


class AdvertiserSerializer(serializers.ModelSerializer):
    package = PackageSerializer(read_only=True)

    class Meta:
        model = Advertiser
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    account_type = AccountTypeSerializer(read_only=True)
    advertiser = AdvertiserSerializer(read_only=True)

    class Meta:
        model = User
        exclude = ('password', 'groups', 'user_permissions', 'is_staff', 'is_superuser', 'last_login', 'date_joined')
        # fields = '__all__'


class CreateUserSerializer(serializers.ModelSerializer):
    account_type = serializers.IntegerField(write_only=True)
    advertiser = serializers.IntegerField(write_only=True)

    class Meta:
        model = User
        # fields = '__all__'
        exclude = (
            'groups', 'user_permissions', 'is_staff', 'is_superuser', 'last_login', 'date_joined',
            'blocked',
            'invoices', 'is_advertiser', 'is_active')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        account_type = validated_data.pop('account_type')
        advertiser = validated_data.pop('advertiser')
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.account_type = AccountType.objects.get(id=account_type)
        user.advertiser = Advertiser.objects.get(id=advertiser)
        user.save()
        return user
