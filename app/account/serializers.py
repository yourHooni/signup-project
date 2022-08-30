from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Account, MobileCarrier


class AccountSerializer(serializers.ModelSerializer):
    log_id = serializers.IntegerField(label='인증 로그 아이디')

    class Meta:
        model = Account
        fields = ('log_id',
                  'name',
                  'nick_name',
                  'email',
                  'password',
                  'mobile_carrier_code',
                  'phone_number',
                  'date_of_birth',
                  'gender')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 8}}


class AccountViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = ('name',
                  'nick_name',
                  'email',
                  'mobile_carrier_code',
                  'phone_number',
                  'date_of_birth',
                  'gender')


class LoginAccountSerializer(serializers.Serializer):
    id = serializers.CharField(label='계정 아이디(이메일 또는 전화번호)')
    password = serializers.CharField(label='계정 비밀번호')


class ResetPasswordSerializer(serializers.Serializer):
    phone_number = serializers.CharField(label='휴대폰 번호')
    log_id = serializers.CharField(label='인증 로그 아이디')
    new_password = serializers.CharField(label='변경할 비밀번호')


class MobileCarrierSerializer(serializers.ModelSerializer):
    class Meta:
        model = MobileCarrier
        fields = ("code", "name")
