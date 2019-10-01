from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    phone = models.CharField(max_length=11)
    birthday = models.DateField(blank=True, null=True)
    portrait = models.URLField(blank=True, null=True)
    credit = models.BooleanField(default=True)
    description = models.TextField(blank=True, null=True)