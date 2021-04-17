from dataclasses import dataclass
import unittest

from wallet_one import Payment


@dataclass
class Data:

    merchant_id = '195751850197'
    secret = '4436657a5c785f354b76314a6c4a666e6832695e58356a5c475c60'
    fail = 'https://localhost.com/fail'
    success = 'https://localhost.com/success'
    description = 'Buy products'
    amount = 1000.00


class TestWalletOnePayment(unittest.TestCase):

    def test_base_case(self):

        case = Payment(
            merchant_id=Data.merchant_id,
            secret=Data.secret,
            amount=Data.amount,
            description=Data.description,
            url_success=Data.success,
            url_fail=Data.fail,
        )
        assert len(case.signature) == 24

        assert case.form['WMI_MERCHANT_ID'] == Data.merchant_id
        assert case.form['WMI_PAYMENT_AMOUNT'] == str(round(Data.amount, 1))
        assert case.form['WMI_CURRENCY_ID'] == '643'
        assert case.form['WMI_DESCRIPTION'] == Data.description
        assert case.form['WMI_SUCCESS_URL'] == Data.success
        assert case.form['WMI_FAIL_URL'] == Data.fail
        assert case.form['WMI_SIGNATURE'] == case.signature

    def test_overloads_case(self):

        prefixed_order_num = 'ORDER-NLE-999'
        payment_name = 'W1RUB'

        case = Payment(
            merchant_id=Data.merchant_id,
            secret=Data.secret,
            amount=Data.amount,
            description=Data.description,
            url_success=Data.success,
            url_fail=Data.fail,
            currency=840,
            override_fields={
                'WMI_PAYMENT_NO': prefixed_order_num,
                'WMI_PTDISABLED': payment_name,
            },
        )

        assert len(case.signature) == 24

        assert case.form['WMI_PAYMENT_NO'] == prefixed_order_num
        assert case.form['WMI_PTDISABLED'] == payment_name


if __name__ == '__main__':
    unittest.main()
