from django.db import models


# Create your models here.
class MobileCarrier(models.Model):
    """Mobile Carrier for phone number"""
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=4, unique=True, blank=False)  # 통신사 코드
    name = models.CharField(max_length=20, blank=False)  # 통신사 명
    created_at = models.DateTimeField(auto_now=True, auto_created=True)
    updated_at = models.DateTimeField(auto_now=True)
