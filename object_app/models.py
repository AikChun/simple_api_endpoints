from django.db import models
from django_unixdatetimefield import UnixDateTimeField

# Create your models here.

class GenericObject(models.Model):
    mykey      = models.CharField(max_length=30)
    value      = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name        = "GenericObject"
        verbose_name_plural = "GenericObjects"

