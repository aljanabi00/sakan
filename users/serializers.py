from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

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


class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    account_type = AccountTypeSerializer(read_only=True)
    advertiser = AdvertiserSerializer(read_only=True)
    invoices = InvoiceSerializer(read_only=True, many=True)

    class Meta:
        model = User
        exclude = ('password', 'groups', 'user_permissions', 'is_staff', 'is_superuser', 'last_login', 'date_joined')
        # fields = '__all__'


# class CreateUserSerializer(serializers.ModelSerializer):
#     account_type = serializers.IntegerField(write_only=True)
#     advertiser = serializers.IntegerField(write_only=True)
#
#     class Meta:
#         model = User
#         # fields = '__all__'
#         exclude = (
#             'groups', 'user_permissions', 'is_staff', 'is_superuser', 'last_login', 'date_joined',
#             'blocked',
#             'invoices', 'is_advertiser', 'is_active')
#         extra_kwargs = {
#             'password': {'write_only': True}
#         }
#
#     def create(self, validated_data):
#         account_type = validated_data.pop('account_type')
#         advertiser = validated_data.pop('advertiser')
#         user = User.objects.create(**validated_data)
#         user.set_password(validated_data['password'])
#         user.account_type = AccountType.objects.get(id=account_type)
#         user.advertiser = Advertiser.objects.get(id=advertiser)
#         user.save()
#         return user
#

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['user'] = UserSerializer(self.user).data
        return data


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('groups', 'user_permissions', 'is_staff', 'is_superuser', 'last_login', 'date_joined', 'blocked',
                   'is_advertiser', 'is_active', 'account_type', 'advertiser', 'first_name', 'last_name', 'email')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        account_type = AccountType.objects.get_or_create(name__contains='باحث', defaults={'name': 'باحث'})
        user.account_type = account_type[0]
        user.is_advertiser = False
        user.save()
        return user


class CreateAdvertiserSerializer(serializers.ModelSerializer):
    advertiser_name = serializers.CharField(write_only=True)

    class Meta:
        model = User
        exclude = ('groups', 'user_permissions', 'is_staff', 'is_superuser', 'last_login', 'date_joined', 'blocked',
                   'is_active', 'is_advertiser', 'account_type', 'first_name', 'last_name', 'email', 'advertiser')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        advertiser_name = validated_data.pop('advertiser_name')
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        account_type = AccountType.objects.get_or_create(name__contains='معلن', defaults={'name': 'معلن'})
        user.account_type = account_type[0]
        user.is_advertiser = True
        package = Package.objects.get_or_create(name__contains='مجاني',
                                                defaults={'name': 'مجاني', 'price': 0, 'can_edit': False,
                                                          'property_limit': 0,
                                                          'repost_limit': 0,
                                                          'featured_limit': 0,
                                                          'property_period': 0,
                                                          'valid_for': 0})
        package = package[0]
        user.advertiser = Advertiser.objects.create(owner_name=advertiser_name, phone=user.phone, package=package)
        user.save()
        return user


class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('groups', 'user_permissions', 'is_staff', 'is_superuser', 'last_login', 'date_joined', 'blocked',
                   'is_active', 'is_advertiser', 'account_type', 'advertiser', 'first_name', 'last_name', 'email',
                   'password')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()
        return instance


class PayPackageSerializer(serializers.ModelSerializer):
    package_id = serializers.IntegerField(write_only=True)
    package_count = serializers.IntegerField(write_only=True)

    class Meta:
        model = User
        fields = ('package_id', 'package_count')
