from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import *


# Register your models here.


class MyUserAdmin(UserAdmin):
    model = User
    list_display = ['username', 'email', 'first_name', 'last_name', 'account_type', 'is_advertiser']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('account_type', 'is_advertiser', 'advertiser', 'image', 'blocked', 'invoices')}),
    )
    filter_horizontal = ('blocked', 'invoices')


class AdvertiserAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner_name', 'phone', 'rating', 'package')


class AccountTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


admin.site.register(AccountType, AccountTypeAdmin)
admin.site.register(Advertiser, AdvertiserAdmin)
admin.site.register(User, MyUserAdmin)
admin.site.register(Package)
admin.site.register(Invoice)
