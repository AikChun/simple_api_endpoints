from django.db import models
from django_unixdatetimefield import UnixDateTimeField
from datetime import datetime
from django.utils import timezone
# Create your models here.

class GenericObject(models.Model):
    mykey      = models.CharField(max_length=30)
    value      = models.TextField()
    created_at = models.DateTimeField(editable=False)
    updated_at = models.DateTimeField(default=datetime.now().strftime('%Y-%m-%dT%H:%M:%'))

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created_at = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        self.updated_at = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        return super(GenericObject, self).save(*args, **kwargs)

    class Meta:
        verbose_name        = "GenericObject"
        verbose_name_plural = "GenericObjects"



