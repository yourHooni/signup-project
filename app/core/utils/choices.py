from django.db import models


class GenderStatus(models.TextChoices):
    """Gender Status for choice"""
    Male = 'M'
    Female = 'F'
