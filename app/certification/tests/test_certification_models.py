"""
    Tests for phone certification models.
"""
import datetime

from django.test import TestCase

from account.models import MobileCarrier
from certification.models import PhoneCertification

mock_mobile_carrier = {
    "code": 3333,
    "name": 'KT'
}

mock_certification = {
    "user_name": '홍길동',
    "mobile_carrier_code": mock_mobile_carrier['code'],
    "phone_number": '01029291111',
    "birth": datetime.datetime(1995, 4, 24),
    "gender": 'm'
}


class PhoneCertificationModelTests(TestCase):
    def setUp(self):
        # create mobile carrier
        self.mobile_carrier = MobileCarrier.objects.create(
            code=mock_mobile_carrier["code"],
            name=mock_mobile_carrier["name"]
        )

    def tearDown(self) -> None:
        pass

    def test_default_certification_values(self):
        """Test default values."""
        certification = PhoneCertification.objects.create(
            user_name=mock_certification["user_name"],
            mobile_carrier_code=MobileCarrier.objects.get(code=mock_certification["mobile_carrier_code"]),
            phone_number=mock_certification["phone_number"],
            date_of_birth=mock_certification["birth"],
            gender=mock_certification["gender"]
        )

        self.assertEqual(certification.user_name, mock_certification["user_name"])
        self.assertEqual(certification.mobile_carrier_code, self.mobile_carrier)
        self.assertEqual(certification.phone_number, mock_certification["phone_number"])
        self.assertEqual(certification.date_of_birth, mock_certification["birth"])
        self.assertEqual(certification.gender, mock_certification["gender"])
