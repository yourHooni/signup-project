"""
    Tests for mobile carrier models.
"""
from django.test import TestCase
from account.models import MobileCarrier

mock_mobile_carrier = {
    "code": 1111,
    "name": 'SK 텔레콤'
}


class MobileCarrierModelTests(TestCase):
    def setUp(self):
        pass

    def tearDown(self) -> None:
        MobileCarrier.objects.all().delete()

    def test_default_mobile_carrier_values(self):
        """Test default values."""
        mobile_carrier = MobileCarrier.objects.create(
            code=mock_mobile_carrier["code"],
            name=mock_mobile_carrier["name"]
        )

        self.assertEqual(mobile_carrier.code, mock_mobile_carrier["code"])
        self.assertEqual(mobile_carrier.name, mock_mobile_carrier["name"])
