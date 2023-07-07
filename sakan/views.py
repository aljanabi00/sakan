import coreapi
import coreschema
from django.db.models import Q
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status, filters
from rest_framework.decorators import api_view
from rest_framework.exceptions import PermissionDenied
from rest_framework.filters import BaseFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Property, Feature, Offer, Province, PropertyType
from .serializers import *


class PropertyListCreateView(generics.ListCreateAPIView):
    queryset = Property.objects.filter(is_visible=True).order_by('-created_at')
    serializer_class = PropertySerializer

    def get_queryset(self):
        try:
            query = self.request.GET['offer']
            if query == 'rent':
                offer = Offer.objects.get(name='للإيجار')
                queryset = Property.objects.filter(for_what=offer, is_visible=True).order_by('-created_at')
                return queryset
            elif query == 'sale':
                offer = Offer.objects.get(name='للبيع')
                queryset = Property.objects.filter(for_what=offer, is_visible=True).order_by('-created_at')
                return queryset
            else:
                return Property.objects.filter(is_visible=True).order_by('-created_at')
        except:
            return Property.objects.filter(is_visible=True).order_by('-created_at')

    # check if the user is authenticated and advertiser to create a property
    def perform_create(self, serializer):
        # if self.request.user.is_authenticated and self.request.user.is_advertiser:
        # check if the property limit is reached
        # if self.request.user.advertiser.is_active is True and Property.objects.filter(
        #         advertiser=self.request.user).count() >= self.request.user.advertiser.package.property_limit:
        #     raise PermissionDenied()
        serializer.save(advertiser=self.request.user)
        # else:
        #     raise PermissionDenied()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if request.user.is_authenticated and request.user.is_advertiser:
            # check if the property limit is reached and the advertiser is active
            try:
                if request.user.advertiser.is_active and request.user.advertiser.property_limit > 0:
                    if serializer.is_valid():
                        if serializer.validated_data['is_featured']:
                            if request.user.advertiser.featured_property_limit > 0:
                                request.user.advertiser.featured_property_limit -= 1
                            else:
                                raise PermissionDenied()
                        self.perform_create(serializer)
                        request.user.advertiser.property_limit -= 1
                        return Response('Property created successfully', status=status.HTTP_201_CREATED)
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                else:
                    raise PermissionDenied()
            except:
                raise PermissionDenied()
        else:
            raise PermissionDenied()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreatePropertySerializer
        return PropertySerializer


class PropertyRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Property.objects.all()
    serializer_class = PropertySerializer

    # check if the user is the owner of the property
    def perform_update(self, serializer):
        if self.request.user == serializer.instance.advertiser:
            serializer.save()
            return Response(serializer.data)
        else:
            raise PermissionDenied()

    def perform_destroy(self, instance):
        if self.request.user == instance.advertiser:
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            raise PermissionDenied()


class FeaturesListView(generics.ListAPIView):
    queryset = Feature.objects.all()
    serializer_class = FeatureSerializer
    pagination_class = None


class FeaturesRetrieveView(generics.RetrieveAPIView):
    queryset = Feature.objects.all()
    serializer_class = FeatureSerializer


@api_view(['GET'])
def get_property_fields(request):
    """
    A function to get the fields required to create a property
    :param request:
    :return:
    """
    try:
        if request.user.is_authenticated and request.user.is_advertiser:
            for_what = Offer.objects.all()
            for_what_serializer = OfferSerializer(for_what, many=True)
            features = Feature.objects.all()
            features_serializer = FeatureSerializer(features, many=True)
            provinces = Province.objects.all()
            provinces_serializer = ProvinceSerializer(provinces, many=True)
            property_types = PropertyType.objects.all()
            property_types_serializer = PropertyTypeSerializer(property_types, many=True)
            return Response({
                'for_what': for_what_serializer.data,
                'property_types': property_types_serializer.data,
                'provinces': provinces_serializer.data,
                'features': features_serializer.data,
            })
        else:
            raise PermissionDenied()
    except:
        raise PermissionDenied()


@api_view(['GET'])
def my_properties(request):
    """
    A function to get the properties of the logged in advertiser
    :param request:
    :return:
    """
    try:
        if request.user.is_authenticated and request.user.is_advertiser:
            properties = Property.objects.filter(advertiser=request.user)
            serializer = PropertySerializer(properties, many=True)
            return Response(serializer.data)
        else:
            raise PermissionDenied()
    except:
        raise PermissionDenied()


class UpdatePropertyStatistics(generics.UpdateAPIView):
    queryset = Statistic.objects.all()
    serializer_class = UpdateStatisticSerializer
    authentication_classes = []
    permission_classes = []

    def perform_update(self, serializer):
        statistic = self.get_object()
        action = self.request.data['action']
        if action == 'visit':
            statistic.visitors += 1
        elif action == 'show_number':
            statistic.show_number += 1
        elif action == 'call':
            statistic.call_number += 1
        elif action == 'whatsapp':
            statistic.whatsapp_number += 1
        elif action == 'message':
            statistic.sms_messages += 1
        elif action == 'share':
            statistic.share += 1
        statistic.save()
        return Response(serializer.data)

    def get_object(self):
        property = Property.objects.get(id=self.kwargs['pk'])
        return property.statistics


class FilterPropertyByType(generics.ListAPIView):
    serializer_class = PropertySerializer

    def get_queryset(self):
        property_type = PropertyType.objects.get(id=self.kwargs['id'])
        return Property.objects.filter(property_type=property_type, is_visible=True).order_by('-created_at')


class FilterPropertyByProvince(generics.ListAPIView):
    serializer_class = PropertySerializer

    def get_queryset(self):
        province = Province.objects.get(id=self.kwargs['id'])
        return Property.objects.filter(province=province, is_visible=True).order_by('-created_at')


class FeaturedPropertiesListView(generics.ListAPIView):
    serializer_class = PropertySerializer

    def get_queryset(self):
        return Property.objects.filter(is_featured=True, is_visible=True).order_by('-created_at')


class PropertyFilter(BaseFilterBackend):
    def get_schema_fields(self, view):
        fields = [
            coreapi.Field(name='price_from', required=False, location='query', schema=coreschema.Integer(),
                          description='price from', type='integer', example=1000000),
            coreapi.Field(name='price_to', required=False, location='query', schema=coreschema.Integer(),
                          description='price to', type='integer', example=1000000),
            coreapi.Field(name='property_type', required=False, location='query', schema=coreschema.Integer(),
                          description='property type', type='integer', example=1),
            coreapi.Field(name='province', required=False, location='query', schema=coreschema.Integer(),
                          description='province', type='integer', example=1),
            coreapi.Field(name='city', required=False, location='query', schema=coreschema.String(), description='city',
                          type='string', example='tehran'),
            coreapi.Field(name='street', required=False, location='query', schema=coreschema.String(),
                          description='street', type='string', example='valiasr'),
            coreapi.Field(name='rooms', required=False, location='query', schema=coreschema.Integer(),
                          description='rooms', type='integer', example=1),
            coreapi.Field(name='bathrooms', required=False, location='query', schema=coreschema.Integer(),
                          description='bathrooms', type='integer', example=1),
            coreapi.Field(name='area', required=False, location='query', schema=coreschema.Integer(),
                          description='area',
                          type='integer', example=100),
            coreapi.Field(name='building_area', required=False, location='query', schema=coreschema.Integer(),
                          description='building area', type='integer', example=100),

        ]
        return fields


class PropertySearchView(generics.ListAPIView):
    """
    A class to search for properties based on the given parameters
    """
    serializer_class = PropertySerializer
    filter_backends = [PropertyFilter]

    def list(self, request, *args, **kwargs):
        filters = Q(is_visible=True)
        price_from = self.request.query_params.get('price_from')
        price_to = self.request.query_params.get('price_to')
        property_type = self.request.query_params.get('property_type')
        province = self.request.query_params.get('province')
        city = self.request.query_params.get('city')
        street = self.request.query_params.get('street')
        rooms = self.request.query_params.get('rooms')
        bathrooms = self.request.query_params.get('bathrooms')
        area = self.request.query_params.get('area')
        building_area = self.request.query_params.get('building_area')

        if price_from:
            filters &= Q(price__gte=price_from)
        if price_to:
            filters &= Q(price__lte=price_to)
        if property_type:
            filters &= Q(property_type=property_type)
        if province:
            filters &= Q(province=province)
        if city:
            filters &= Q(city__search=city)
        if street:
            filters &= Q(street__search=street)
        if rooms:
            filters &= Q(rooms=rooms)
        if bathrooms:
            filters &= Q(bathrooms=bathrooms)
        if area:
            filters &= Q(area=area)
        if building_area:
            filters &= Q(building_area=building_area)

        properties = Property.objects.filter(filters)
        properties = properties.order_by('-created_at')

        page = self.paginate_queryset(properties)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(properties, many=True)
        return Response(serializer.data)
