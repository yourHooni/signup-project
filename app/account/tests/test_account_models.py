"""
    Tests for phone certification models.
"""
import datetime

from django.test import TestCase

from account.models import Account, MobileCarrier

mock_mobile_carrier = {
    "code": 3333,
    "name": 'KT'
}

mock_account = {
    "name": '홍길동',
    "nick_name": '길똥',
    "email": 'rlfehd@gmail.com',
    "password": '1234',
    "mobile_carrier_code": mock_mobile_carrier['code'],
    "phone_number": '01029291111',
    "birth": datetime.datetime(1995, 4, 24),
    "gender": 'm'
}


class AccountModelTests(TestCase):
    def setUp(self):
        # create mobile carrier
        self.mobile_carrier = MobileCarrier.objects.create(
            code=mock_mobile_carrier["code"],
            name=mock_mobile_carrier["name"]
        )

    def tearDown(self) -> None:
        Account.objects.all().delete()
        MobileCarrier.objects.all().delete()

    def test_default_account_values(self):
        """Test default values."""
        account = Account.objects.create(
            name=mock_account["name"],
            nick_name=mock_account["nick_name"],
            email=mock_account["email"],
            password=mock_account["password"],
            mobile_carrier_code=MobileCarrier.objects.get(code=mock_account["mobile_carrier_code"]),
            phone_number=mock_account["phone_number"],
            date_of_birth=mock_account["birth"],
            gender=mock_account["gender"]
        )

        self.assertEqual(account.name, mock_account["name"])
        self.assertEqual(account.nick_name, mock_account["nick_name"])
        self.assertEqual(account.email, mock_account["email"])
        self.assertEqual(account.password, mock_account["password"])
        self.assertEqual(account.mobile_carrier_code, self.mobile_carrier)
        self.assertEqual(account.phone_number, mock_account["phone_number"])
        self.assertEqual(account.date_of_birth, mock_account["birth"])
        self.assertEqual(account.gender, mock_account["gender"])
