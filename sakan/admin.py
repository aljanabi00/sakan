from django.contrib import admin
from .models import *


# Register your models here.


class PropertyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'for_what', 'advertiser')
    list_filter = ('for_what', 'features')
    search_fields = ('name', 'price', 'for_what', 'advertiser')


class FeatureAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


admin.site.register(Image)
admin.site.register(Feature, FeatureAdmin)
admin.site.register(Property, PropertyAdmin)
admin.site.register(Offer)