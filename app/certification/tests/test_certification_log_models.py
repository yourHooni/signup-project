"""
    Tests for phone certification models.
"""
import datetime

from django.test import TestCase

from account.models import MobileCarrier
from certification.models import PhoneCertification, PhoneCertificationLog

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

mock_certification_log = {
    "code": '415623',
}


class PhoneCertificationModelTests(TestCase):
    def setUp(self):
        # create phone certification
        MobileCarrier.objects.create(
            code=mock_mobile_carrier["code"],
            name=mock_mobile_carrier["name"]
        )

        self.certification = PhoneCertification.objects.create(
            user_name=mock_certification["user_name"],
            mobile_carrier_code=MobileCarrier.objects.get(code=mock_certification["mobile_carrier_code"]),
            phone_number=mock_certification["phone_number"],
            date_of_birth=mock_certification["birth"],
            gender=mock_certification["gender"]
        )

    def tearDown(self) -> None:
        pass

    def test_default_certification_log_values(self):
        """Test default values."""
        log = PhoneCertificationLog.objects.create(
            phone_certification_id=self.certification,
            code=mock_certification_log["code"]
        )

        self.assertEqual(log.id, self.certification.id)
        self.assertEqual(log.code, mock_certification_log["code"])
