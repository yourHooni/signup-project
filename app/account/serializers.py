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


class LoginAccountSerializer(serializers.Serializer):
    id = serializers.CharField(label='계정 아이디(이메일 또는 전화번호)')
    password = serializers.CharField(label='계정 비밀번호')

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Unable to log in with provided credentials.")


class MobileCarrierSerializer(serializers.ModelSerializer):
    class Meta:
        model = MobileCarrier
        fields = ("code", "name")
