from rest_framework import serializers

from users.serializers import UserSerializer
from .models import *


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('image',)


class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = '__all__'


class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = '__all__'


class ProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        fields = '__all__'


class PropertyTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyType
        fields = '__all__'


class PropertySerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)
    features = FeatureSerializer(many=True, read_only=True)
    for_what = OfferSerializer(read_only=True)
    advertiser = UserSerializer(read_only=True)
    property_type = PropertyTypeSerializer(read_only=True)
    province = ProvinceSerializer(read_only=True)

    class Meta:
        model = Property
        fields = '__all__'


class CreatePropertySerializer(serializers.ModelSerializer):
    images = serializers.ListField(child=serializers.ImageField(), write_only=True)
    features = serializers.ListField(child=serializers.IntegerField(), write_only=True)
    for_what = serializers.IntegerField(write_only=True)
    province = serializers.IntegerField(write_only=True)
    property_type = serializers.IntegerField(write_only=True)

    class Meta:
        model = Property
        exclude = ('is_visible', 'created_at', 'advertiser')
        extra_kwargs = {
            'advertiser': {'read_only': True},
        }

    def create(self, validated_data):
        images_data = validated_data.pop('images', [])
        features_data = validated_data.pop('features', [])
        for_what = validated_data.pop('for_what', None)
        property_type = validated_data.pop('property_type', None)
        province = validated_data.pop('province', None)
        property = Property.objects.create(**validated_data)
        for image_data in images_data:
            image = Image.objects.create(image=image_data)
            property.images.add(image)
        property.features.add(*features_data)
        property.for_what = Offer.objects.get(id=for_what)
        property.property_type = PropertyType.objects.get(id=property_type)
        property.province = Province.objects.get(id=province)
        property.save()
        return property
