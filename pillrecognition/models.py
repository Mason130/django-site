from django.db import models
from .storage import OverwriteStorage


class PillsInformation(models.Model):
    ndc11 = models.CharField(max_length=200)
    rxcui = models.IntegerField(null=False, default=0)
    pill_name = models.CharField(max_length=200)
    generic_name = models.CharField(max_length=200)

    def __str__(self):
        return self.pill_name


class UploadImage(models.Model):
    pill_image = models.ImageField(max_length=255, upload_to='uploaded_pill',
                                   default="uploaded_pill/default.png",
                                   storage=OverwriteStorage(),
                                   null=True, blank=True)
