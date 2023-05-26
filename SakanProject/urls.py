"""
URL configuration for SakanProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

schema_view = get_schema_view(
    openapi.Info(
        title="Sakan API",
        default_version='v1',
        description="API Documentation",
    ),
    public=True,
)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('property/', include('sakan.urls')),
    path('auth/', include('users.urls')),

    path('swagger<str:format>', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]

# add media url

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# add static url

# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)