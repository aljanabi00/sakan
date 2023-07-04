from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.exceptions import PermissionDenied
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
        property_type = PropertyType.objects.get(id=self.kwargs['pk'])
        return Property.objects.filter(property_type=property_type, is_visible=True).order_by('-created_at')


class FilterPropertyByProvince(generics.ListAPIView):
    serializer_class = PropertySerializer

    def get_queryset(self):
        province = Province.objects.get(id=self.kwargs['pk'])
        return Property.objects.filter(province=province, is_visible=True).order_by('-created_at')


class FeaturedPropertiesListView(generics.ListAPIView):
    serializer_class = PropertySerializer

    def get_queryset(self):
        return Property.objects.filter(is_featured=True, is_visible=True).order_by('-created_at')
