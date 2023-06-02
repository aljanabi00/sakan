from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.


class Package(models.Model):
    name = models.CharField(max_length=200)
    price = models.IntegerField(default=0)
    property_limit = models.IntegerField(default=0)
    repost_limit = models.IntegerField(default=0)
    featured_limit = models.IntegerField(default=0)
    property_period = models.IntegerField(default=0)
    valid_for = models.IntegerField(default=0)
    can_edit = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Invoice(models.Model):
    amount = models.IntegerField(default=0)
    package = models.ForeignKey(Package, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return self.package.name + ' - ' + str(self.amount)


class AccountType(models.Model):
    name = models.CharField(max_length=200)

    # property_limit = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Advertiser(models.Model):
    office = models.CharField(max_length=255, null=True, blank=True)
    owner_name = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    location = models.URLField(null=True, blank=True)
    rating = models.IntegerField(default=0)
    package = models.ForeignKey(Package, on_delete=models.CASCADE, null=True, blank=True)
    invoices = models.ManyToManyField(Invoice, blank=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.owner_name


class User(AbstractUser):
    phone = models.CharField(max_length=16, null=True, blank=True)
    account_type = models.ForeignKey(AccountType, on_delete=models.CASCADE, null=True, blank=True)
    is_advertiser = models.BooleanField(default=False)
    advertiser = models.ForeignKey(Advertiser, on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    blocked = models.ManyToManyField('self', blank=True)
