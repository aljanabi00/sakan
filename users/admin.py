from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

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
    list_display = ('id', 'owner_name', 'phone', 'rating', 'package', 'is_active')
    filter_horizontal = ('invoices',)


class AccountTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


admin.site.register(AccountType, AccountTypeAdmin)
admin.site.register(Advertiser, AdvertiserAdmin)
admin.site.register(User, MyUserAdmin)
admin.site.register(Package)
admin.site.register(Invoice)

admin.site.site_header = 'Sakan Admin Panel'
admin.site.site_title = 'Sakan Admin Panel'
admin.site.index_title = 'Sakan Admin Panel'
