from rest_framework import serializers

from .models import PhoneCertification, PhoneCertificationLog


class PhoneCertificationSerializer(serializers.ModelSerializer):
    """Serializer for phone certification objects."""
    class Meta:
        model = PhoneCertification
        fields = ('user_name',
                  'mobile_carrier_code',
                  'phone_number',
                  'date_of_birth',
                  'gender')


class CheckCertificationCodeSerializer(serializers.ModelSerializer):
    """Serializer for phone certification log objects."""
    log_id = serializers.IntegerField(label='인증 로그 아이디')

    class Meta:
        model = PhoneCertificationLog
        fields = ('log_id', 'code')



