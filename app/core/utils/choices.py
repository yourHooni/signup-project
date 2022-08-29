from django.db import models


class GenderStatus(models.TextChoices):
    """Gender Status for choice"""
    M = 'Male'
    F = 'Female'
