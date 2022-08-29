from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Account, MobileCarrier


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('name',
                  'nick_name',
                  'email',
                  'password',
                  'mobile_carrier_code',
                  'phone_number',
                  'date_of_birth',
                  'gender')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 8}}



class MobileCarrierSerializer(serializers.ModelSerializer):
    class Meta:
        model = MobileCarrier
        fields = ("code", "name")
