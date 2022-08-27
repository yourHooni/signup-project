from django.db import models


# Create your models here.
class MobileCarrier(models.Model):
    """Mobile Carrier for phone number"""
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=4, unique=True, blank=False)  # 통신사 코드
    name = models.CharField(max_length=20, blank=False)  # 통신사 명
    created_at = models.DateTimeField(auto_now=True, auto_created=True)
    updated_at = models.DateTimeField(auto_now=True)


class PhoneCertification(models.Model):
    """Phone Certification for user Certification"""
    # 성별
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

    id = models.AutoField(primary_key=True)
    mobile_carrier_code = models.CharField(max_length=4, blank=False)  # 통신사 코드
    phone_number = models.CharField(max_length=20, blank=False)  # 휴대폰 번호
    user_name = models.CharField(max_length=4, blank=False)  # 사용자 명
    birth = models.CharField(max_length=6, blank=False)  # 사용자 생년월일
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=False)  # 사용자 성별
    created_at = models.DateTimeField(auto_now=True, auto_created=True)
    updated_at = models.DateTimeField(auto_now=True)
