"""
    Tests for mobile carrier models.
"""
from django.test import TestCase

from phone_certification.models import MobileCarrier, PhoneCertification

mock_mobile_carrier = {
    "code": 2222,
    "name": 'LG U+'
}

mock_phone_certification = {
    "mobile_carrier_code": 2222,
    "phone_number": "01029291111",
    "user_name": "홍길동",
    "birth": "951010",
    "gender": "m"
}


class PhoneCertificationModelTests(TestCase):
    def test_default_mobile_carrier_values(self):
        """Test default values."""
        # create mobile carrier
        MobileCarrier.objects.create(
            code=mock_mobile_carrier["code"],
            name=mock_mobile_carrier["name"]
        )

        phone_certification = PhoneCertification.objects.create(
            mobile_carrier_code=mock_phone_certification["mobile_carrier_code"],
            phone_number=mock_phone_certification["phone_number"],
            user_name=mock_phone_certification["user_name"],
            birth=mock_phone_certification["birth"],
            gender=mock_phone_certification["gender"]
        )

        self.assertEqual(phone_certification.mobile_carrier_code, mock_phone_certification["mobile_carrier_code"])
        self.assertEqual(phone_certification.phone_number, mock_phone_certification["phone_number"])
        self.assertEqual(phone_certification.user_name, mock_phone_certification["user_name"])
        self.assertEqual(phone_certification.birth, mock_phone_certification["birth"])
        self.assertEqual(phone_certification.gender, mock_phone_certification["gender"])




