from django.db import models


# Create your models here.

class Image(models.Model):
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return str(self.id)


class Feature(models.Model):
    name = models.CharField(max_length=200)
    en_name = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    icon = models.ImageField(upload_to='icons/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Offer(models.Model):
    name = models.CharField(max_length=255)
    en_name = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name


class PropertyType(models.Model):
    name = models.CharField(max_length=255)
    en_name = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name


class Province(models.Model):
    name = models.CharField(max_length=255)
    en_name = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name


class Status(models.Model):
    name = models.CharField(max_length=255)
    en_name = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name

    @classmethod
    def get_default_pk(cls):
        return Status.objects.get_or_create(en_name='pending', name='قيد التدقيق')[0].pk


class Statistic(models.Model):
    price = models.IntegerField(default=0)
    name = models.CharField(max_length=255, null=True, blank=True)
    en_name = models.CharField(max_length=255, null=True, blank=True)
    visitors = models.IntegerField(default=0)
    show_number = models.IntegerField(default=0)
    call_number = models.IntegerField(default=0)
    whatsapp_number = models.IntegerField(default=0)
    sms_messages = models.IntegerField(default=0)
    share = models.IntegerField(default=0)
    status = models.ForeignKey(Status, on_delete=models.CASCADE, null=True, blank=True,
                               default=Status.get_default_pk)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'statistic for ' + str(self.id)


class Property(models.Model):
    name = models.CharField(max_length=255)
    price = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    en_description = models.TextField(null=True, blank=True)
    cover = models.ImageField(upload_to='covers/')
    images = models.ManyToManyField(Image, blank=True)
    video = models.URLField(null=True, blank=True)
    location = models.URLField(null=True, blank=True)
    for_what = models.ForeignKey(Offer, on_delete=models.CASCADE, null=True, blank=True)
    property_type = models.ForeignKey(PropertyType, on_delete=models.CASCADE, null=True, blank=True)
    category = models.CharField(max_length=255, null=True, blank=True)
    province = models.ForeignKey(Province, on_delete=models.CASCADE, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    street = models.CharField(max_length=255, null=True, blank=True)
    property_number = models.CharField(max_length=255, null=True, blank=True)
    rooms = models.IntegerField(null=True, blank=True)
    bathrooms = models.IntegerField(null=True, blank=True)
    area = models.IntegerField(null=True, blank=True)
    building_area = models.IntegerField(null=True, blank=True)
    features = models.ManyToManyField(Feature, blank=True, related_name="feature")
    advertiser = models.ForeignKey('users.User', on_delete=models.CASCADE)
    is_visible = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    statistics = models.ForeignKey(Statistic, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Properties'
