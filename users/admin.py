from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.http import HttpResponseRedirect

from .models import *


# Register your models here.


class MyUserAdmin(UserAdmin):
    model = User
    list_display = ['username', 'account_type', 'is_advertiser']
    fieldsets = (
        ['User', {'fields': ('username', 'password')}],
        ('Personal info', {'fields': ('phone', 'image')}),
        ('Sakan', {'fields': ('account_type', 'is_advertiser', 'advertiser', 'blocked')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    filter_horizontal = ('blocked',)


class AdvertiserAdmin(admin.ModelAdmin):
    change_form_template = 'advertiser.html'
    list_display = ('id', 'owner_name', 'phone', 'rating', 'package', 'package_requested_at', 'is_active')
    filter_horizontal = ('invoices',)

    def response_change(self, request, obj):
        if "_pay" in request.POST:
            obj.package_paid_at = datetime.now()
            obj.package_expires_at = datetime.now() + relativedelta(months=obj.package.valid_for)
            obj.is_active = True
            obj.invoices.add(Invoice.objects.create(amount=obj.package.price, package=obj.package, is_paid=True))
            obj.save()
            return HttpResponseRedirect(".")


class AccountTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


class PackageAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'property_limit', 'repost_limit', 'featured_limit', 'property_period',
                    'valid_for', 'can_edit')


admin.site.register(AccountType, AccountTypeAdmin)
admin.site.register(Advertiser, AdvertiserAdmin)
admin.site.register(User, MyUserAdmin)
admin.site.register(Package, PackageAdmin)
admin.site.register(Invoice)

admin.site.site_header = 'Sakan Admin Panel'
admin.site.site_title = 'Sakan Admin Panel'
admin.site.index_title = 'Sakan Admin Panel'
