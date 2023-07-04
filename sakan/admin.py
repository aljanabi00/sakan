from datetime import datetime

from dateutil.relativedelta import relativedelta
from django.contrib import admin
from django.http import HttpResponseRedirect

from .models import *


# Register your models here.


class PropertyAdmin(admin.ModelAdmin):
    change_form_template = 'property.html'
    list_display = ('id', 'name', 'price', 'for_what', 'advertiser')
    list_filter = ('for_what', 'features')
    search_fields = ('name', 'price', 'for_what', 'advertiser')
    list_display_links = ('id', 'name')
    filter_horizontal = ('features', 'images')

    def response_change(self, request, obj):
        if "_post_property" in request.POST:
            obj.is_visible = True
            obj.expires_at = datetime.now() + relativedelta(months=obj.advertiser.advertiser.package.property_period)
            obj.save()
            return HttpResponseRedirect(".")
        return super().response_change(request, obj)


class FeatureAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


class ProvinceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


class PropertyTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


class OfferAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


class StatisticAdmin(admin.ModelAdmin):
    list_display = ('id', 'visitors', 'show_number', 'call_number', 'whatsapp_number', 'sms_messages', 'share', 'status')


admin.site.register(Image)
admin.site.register(Feature, FeatureAdmin)
admin.site.register(Property, PropertyAdmin)
admin.site.register(Offer, OfferAdmin)
admin.site.register(Province, ProvinceAdmin)
admin.site.register(PropertyType, PropertyTypeAdmin)
admin.site.register(Status)
admin.site.register(Statistic)
