from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework_simplejwt.views import TokenObtainPairView


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class PackageListView(generics.ListAPIView):
    queryset = Package.objects.all()
    serializer_class = PackageSerializer
    pagination_class = None


class AccountTypeListView(generics.ListAPIView):
    queryset = AccountType.objects.all()
    serializer_class = AccountTypeSerializer
    pagination_class = None


class CreateUserView(generics.CreateAPIView):
    serializer_class = CreateUserSerializer
    queryset = User.objects.all()
    authentication_classes = ()
    permission_classes = ()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            data = MyTokenObtainPairSerializer.validate(MyTokenObtainPairSerializer(), attrs={
                'username': user.username,
                'password': request.data['password']
            })
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save()
        return Response(serializer.data)


class CreateAdvertiserView(generics.CreateAPIView):
    serializer_class = CreateAdvertiserSerializer
    queryset = Advertiser.objects.all()
    authentication_classes = ()
    permission_classes = ()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            advertiser = serializer.save()
            data = MyTokenObtainPairSerializer.validate(MyTokenObtainPairSerializer(), attrs={
                'username': advertiser.username,
                'password': request.data['password']
            })
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save()
        return Response(serializer.data)


class MyAccountView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class MyAccountUpdateView(generics.UpdateAPIView):
    serializer_class = UpdateUserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = UserSerializer(user)
            return Response(response.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PackageView(generics.ListAPIView):
    """
    A view to list all packages.
    """
    serializer_class = PackageSerializer
    permission_classes = [IsAuthenticated]
    queryset = Package.objects.all()


class PayPackageView(generics.CreateAPIView):
    """
    A view to pay for a package that takes a package id and a package count.
    """
    serializer_class = PayPackageSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        body = request.data
        package = Package.objects.get(id=body['package_id'])
        if request.user.is_authenticated and request.user.is_advertiser:
            advertiser = Advertiser.objects.get(user=request.user)
            if package != advertiser.package:
                advertiser.package = package
            for i in range(body['package_count']):
                advertiser.package_count += 1
                advertiser.property_limit += package.property_limit
                advertiser.repost_limit += package.repost_limit
                advertiser.featured_limit += package.featured_limit

            advertiser.property_period = package.property_period
            advertiser.save()
            return Response('Package paid successfully', status=status.HTTP_200_OK)
        else:
            raise PermissionDenied()
