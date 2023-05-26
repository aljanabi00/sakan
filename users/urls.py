from django.urls import include, path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from users.views import PackageListView, AccountTypeListView, CreateUserView

urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('packages/', PackageListView.as_view()),
    path('account-types/', AccountTypeListView.as_view()),
    path('create-account/', CreateUserView.as_view()),

]
