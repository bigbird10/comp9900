from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    phone = models.CharField(max_length=11)
    birthday = models.DateField(blank=True, null=True)
    portrait = models.URLField(blank=True, null=True)
    credit = models.BooleanField(default=True)
    description = models.TextField(blank=True, null=True)


class Listing(models.Model):
    id = models.AutoField(primary_key=True)
    host_id = models.BigIntegerField()
    property_type = models.CharField(blank=True, max_length=50, null=True)
    room_type = models.CharField(blank=True, max_length=50, null=True)
    accommodates = models.IntegerField(blank=True, null=True)
    bedrooms = models.IntegerField(blank=True, null=True)
    beds = models.IntegerField(blank=True, null=True)
    bathrooms = models.FloatField(blank=True, null=True)
    street = models.CharField(blank=True, max_length=200, null=True)
    city = models.CharField(blank=True, max_length=50, null=True)
    state = models.CharField(blank=True, max_length=50, null=True)
    zipcode = models.IntegerField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    amenities = models.TextField(blank=True, null=True)
    summary = models.TextField(blank=True, null=True)
    transit = models.TextField(blank=True, null=True)
    neighborhood = models.TextField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    price = models.DecimalField(decimal_places=1, max_digits=6, blank=True, null=True)
    '''picture = models.URLField(blank=True, null=True)'''


class Scene(models.Model):
    listing_id = models.BigIntegerField()
    picture = models.URLField(blank=True, null=True)


class Calendar(models.Model):
    listing_id = models.BigIntegerField()