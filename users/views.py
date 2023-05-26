from rest_framework import generics, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from .models import *
from .serializers import *


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

    def perform_create(self, serializer):
        serializer.save()
        return Response(serializer.data)
