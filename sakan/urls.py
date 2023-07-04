from django.urls import path
from .views import *

urlpatterns = [
    path('', PropertyListCreateView.as_view()),
    path('my-properties/', my_properties, name='my-properties'),
    path('<int:pk>/', PropertyRetrieveUpdateDestroyView.as_view()),
    path('features/', FeaturesListView.as_view()),
    path('features/<int:pk>/', FeaturesRetrieveView.as_view()),
    path('fields/', get_property_fields),
    path('update-statistics/<int:pk>/', UpdatePropertyStatistics.as_view()),
    path('filter-properties-type/<int:pk>/', FilterPropertyByType.as_view()),
    path('filter-properties-province/<int:pk>/', FilterPropertyByProvince.as_view()),
    path('featured-properties/', FeaturedPropertiesListView.as_view()),
]
