"""
    Tests for mobile carrier models.
"""
from django.test import TestCase
from phone_certification.models import MobileCarrier


class MobileCarrierModelTests(TestCase):
    def test_default_mobile_carrier_values(self):
        """Test default values."""
        mock_code = 1
        mock_name = 'SK 텔레콤'

        mobile_carrier = MobileCarrier.objects.create(
            code=mock_code,
            name=mock_name
        )

        self.assertEqual(mobile_carrier.code, mock_code)
        self.assertEqual(mobile_carrier.name, mock_name)


