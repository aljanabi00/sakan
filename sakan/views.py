from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from .models import Property, Feature, Offer
from .serializers import PropertySerializer, FeatureSerializer, OfferSerializer, CreatePropertySerializer


class PropertyListCreateView(generics.ListCreateAPIView):
    queryset = Property.objects.filter(is_visible=True).order_by('-created_at')
    serializer_class = PropertySerializer

    # check if the user is authenticated and advertiser to create a property
    def perform_create(self, serializer):
        if self.request.user.is_authenticated and self.request.user.is_advertiser:
            # check if the property limit is reached
            if self.request.user.advertiser.is_active is True and Property.objects.filter(
                    advertiser=self.request.user).count() >= self.request.user.advertiser.package.property_limit:
                raise PermissionDenied()
            serializer.save(advertiser=self.request.user)
        else:
            raise PermissionDenied()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if request.user.is_authenticated and request.user.is_advertiser:
            if request.user.advertiser.is_active and Property.objects.filter(
                    advertiser=request.user).count() <= request.user.advertiser.package.property_limit:
                if serializer.is_valid():
                    self.perform_create(serializer)
                    return Response('Property created successfully', status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                raise PermissionDenied()
        else:
            raise PermissionDenied()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreatePropertySerializer
        return PropertySerializer


class PropertyRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
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
            return Response({
                'for_what': for_what_serializer.data,
                'features': features_serializer.data
            })
        else:
            raise PermissionDenied()
    except:
        raise PermissionDenied()
