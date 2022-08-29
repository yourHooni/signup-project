from django.db import models

from core.utils.choices import GenderStatus


class Account(models.Model):
    """User Account"""
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, verbose_name='사용자 명')
    nick_name = models.CharField(max_length=100, unique=True, verbose_name='닉네임')
    email = models.EmailField(unique=True, verbose_name='이메일')
    password = models.CharField(max_length=500, verbose_name='비밀번호')
    mobile_carrier_code = models.ForeignKey('account.MobileCarrier', on_delete=models.CASCADE,
                                            db_column='mobile_carrier_code', to_field='code', verbose_name='통신사 코드')
    phone_number = models.CharField(max_length=20, verbose_name='휴대폰 번호')
    date_of_birth = models.DateField(verbose_name='생년월일')
    gender = models.CharField(max_length=10, choices=GenderStatus.choices, verbose_name='성별')
    created_at = models.DateTimeField(auto_now=True, auto_created=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nick_name

    def create(self, name, nick_name, email, password, mobile_carrier_code, phone_number, date_of_birth, gender):
        self.name = name
        self.nick_name = nick_name
        self.email = email
        self.password = password
        self.mobile_carrier_code = mobile_carrier_code
        self.phone_number = phone_number
        self.date_of_birth = date_of_birth
        self.gender = gender


class MobileCarrier(models.Model):
    """Mobile Carrier for phone number"""
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=4, unique=True, verbose_name='통신사 코드')
    name = models.CharField(max_length=20, verbose_name='통신사 명')
    created_at = models.DateTimeField(auto_now=True, auto_created=True)
    updated_at = models.DateTimeField(auto_now=True)
