from __future__ import unicode_literals
import os
from django.conf import settings
from django.shortcuts import render_to_response
from django.test import TestCase
from paypal.standard.pdt.models import PayPalPDT
from decimal import Decimal
import mock
from django.contrib.auth import get_user_model
from django.forms import ValidationError
from django.test.client import RequestFactory
from django.test.utils import override_settings
from vcr import VCR
from paypal.pro.exceptions import PayPalFailure
from paypal.pro.fields import CreditCardField
from paypal.pro.helpers import VERSION, PayPalError, PayPalWPP, strip_ip_port
from paypal.pro.views import PayPalPro


class DummyPayPalPDT(object):

    def __init__(self, update_context_dict={}):
        self.context_dict = {'st': 'SUCCESS', 'custom': 'cb736658-3aad-4694-956f-d0aeade80194',
                             'txn_id': '1ED550410S3402306', 'mc_gross': '225.00',
                             'txn_id': '1ED550410S3402306', 'mc_gross': '225.00',
                             'business': settings.PAYPAL_RECEIVER_EMAIL, 'error': 'Error code: 1234'}

        self.context_dict.update(update_context_dict)

    def update_with_get_params(self, get_params):
        if 'tx' in get_params:
            self.context_dict['txn_id'] = get_params.get('tx')
        if 'amt' in get_params:
            self.context_dict['mc_gross'] = get_params.get('amt')
        if 'cm' in get_params:
            self.context_dict['custom'] = get_params.get('cm')

    def _postback(self, test=True):
        """Perform a Fake PayPal PDT Postback request."""
        # @@@ would be cool if this could live in the test templates dir...
        return render_to_response("payment/done.html", self.context_dict).content


class PDTTest(TestCase):
    urls = "paypal.standard.pdt.tests.test_urls"
    template_dirs = [os.path.join(os.path.dirname(__file__), 'templates'), ]

    def setUp(self):
        # set up some dummy PDT get parameters
        self.get_params = {"tx": "4WJ86550014687441", "st": "Completed", "amt": "225.00", "cc": "EUR",
                           "cm": "a3e192b8-8fea-4a86-b2e8-d5bf502e36be", "item_number": "",
                           "sig": "blahblahblah"}

        # monkey patch the PayPalPDT._postback function
        self.dpppdt = DummyPayPalPDT()
        self.dpppdt.update_with_get_params(self.get_params)
        PayPalPDT._postback = self.dpppdt._postback

    def test_verify_postback(self):
        dpppdt = DummyPayPalPDT()
        paypal_response = dpppdt._postback()
        self.assertEqual(len(PayPalPDT.objects.all()), 0)
        pdt_obj = PayPalPDT()
        pdt_obj.ipaddress = '127.0.0.1'
        pdt_obj.response = paypal_response
        self.assertEqual(len(PayPalPDT.objects.all()), 0)

#from .settings import TEMPLATES

RF = RequestFactory()

vcr = VCR(path_transformer=VCR.ensure_suffix('.yaml'))


def make_request(user=None):
    request = RF.get("/pay/", REMOTE_ADDR="127.0.0.1:8000")
    if user is not None:
        request.user = user
    return request


class CreditCardFieldTest(TestCase):
    def test_CreditCardField(self):
        field = CreditCardField()
        field.clean('4797503429879309')
        self.assertEqual(field.card_type, "Visa")
        self.assertRaises(ValidationError, CreditCardField().clean, '1234567890123455')

    def test_invalidCreditCards(self):
        self.assertEqual(CreditCardField().clean('4797-5034-2987-9309'), '4797503429879309')