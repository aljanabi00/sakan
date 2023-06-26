from django.urls import include, path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from users.views import *

urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    # path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('my-account/', MyAccountView.as_view(), name='my-account'),

    path('packages/', PackageListView.as_view()),
    path('account-types/', AccountTypeListView.as_view()),
    path('create-user/', CreateUserView.as_view()),
    path('create-advertiser/', CreateAdvertiserView.as_view()),

    path('packages/', PackageListView.as_view(), name='packages'),
    path('packages/pay/', PayPackageView.as_view(), name='pay-package'),

]
