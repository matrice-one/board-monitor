from django.db import models

# Create your models here.
from django.core import validators

# Create your models here.
class historic(models.Model):
    id = models.BigAutoField(
        primary_key=True
    )

    name_surname = models.CharField(
        max_length=70,
        verbose_name='Name and surname'
    )

    origin = models.CharField(
        max_length=800,
        verbose_name='Origin'
    )

    destination = models.CharField(
        max_length=800,
        verbose_name='Destination'
    )

    status = models.CharField(
        max_length=800,
        verbose_name='Status'
    )

    signature_mode = models.CharField(
        max_length=800,
        verbose_name='Signature Mode'
    )

    company = models.CharField(
        max_length=800,
        verbose_name='Company'
    )


