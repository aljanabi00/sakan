from rest_framework import generics, status
from rest_framework.exceptions import PermissionDenied
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
