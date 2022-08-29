from django.db import models

from core.utils.choices import GenderStatus


# Create your models here.
class PhoneCertification(models.Model):
    """for phone certification"""
    id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=100, verbose_name='성함')
    mobile_carrier_code = models.ForeignKey('account.MobileCarrier', on_delete=models.CASCADE,
                                            db_column='mobile_carrier_code', to_field='code', verbose_name='통신사 코드')
    phone_number = models.CharField(max_length=20, verbose_name='휴대폰 번호')
    date_of_birth = models.DateField(verbose_name='생년월일')
    gender = models.CharField(max_length=10, choices=GenderStatus.choices, verbose_name='성별')
    created_at = models.DateTimeField(auto_now=True, auto_created=True)
    updated_at = models.DateTimeField(auto_now=True)


class PhoneCertificationLog(models.Model):
    """Certification log"""
    id = models.AutoField(primary_key=True)
    phone_certification_id = models.OneToOneField('certification.PhoneCertification',
                                                  on_delete=models.CASCADE, db_column='phone_certification_id',
                                                  verbose_name='휴대폰 인증 id')
    code = models.CharField(max_length=6, verbose_name='인증 코드')
    is_certificated = models.BooleanField(default=False, verbose_name='인증 여부')
    created_at = models.DateTimeField(auto_now=True, auto_created=True)
    updated_at = models.DateTimeField(auto_now=True)
