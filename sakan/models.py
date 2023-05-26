from django.db import models


# Create your models here.

class Image(models.Model):
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return str(self.id)


class Feature(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    icon = models.ImageField(upload_to='icons/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Offer(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Property(models.Model):
    name = models.CharField(max_length=255)
    price = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    cover = models.ImageField(upload_to='covers/')
    images = models.ManyToManyField(Image, blank=True)
    video = models.URLField(null=True, blank=True)
    location = models.URLField(null=True, blank=True)
    for_what = models.ForeignKey(Offer, on_delete=models.CASCADE, null=True, blank=True)
    features = models.ManyToManyField(Feature, blank=True, related_name="feature")
    advertiser = models.ForeignKey('users.User', on_delete=models.CASCADE)
    is_visible = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Properties'
