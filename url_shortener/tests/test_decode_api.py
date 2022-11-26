"""
    It contains the Decode API test cases.

"""
import os
import sys

import django
from importlib import reload

reload(sys)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR + '/short_link')
os.environ['DJANGO_SETTINGS_MODULE'] = 'cron_server'
sys.path.append(BASE_DIR)
django.setup()
from django.test import TestCase, Client
from urllib.parse import urlencode

client = Client()


class DecodeAPITest(TestCase):
    """
    Test module for Decode API

    """

    def setUp(self):

        self.payload_encode_positive = {'original_url': 'google.com'}
        self.payload_decode_positive = {}
        self.payload_negative = {'short_url': '0000001'}
        self.supported_api_versions = ['1.0']
        self._content_type_value = 'application/json; version='

    def test_decode_api_response_positive(self):
        """
        Positive test cases with valid input and valid expected and actual output.

        """
        encode_response = client.post(
            '/shorturl/encode/',
            data=urlencode(self.payload_encode_positive),
            content_type='application/x-www-form-urlencoded'
        )

        self.payload_decode_positive['short_url'] = encode_response.data['short_url']

        response = client.post(
            '/shorturl/decode/',
            data=urlencode(self.payload_decode_positive),
            content_type='application/x-www-form-urlencoded'
        )

        # Testing positive test cases
        assert response.status_code == 200
        assert response.data['status'] == 'True'
        assert response.data['original_url'] == self.payload_encode_positive['original_url']

    def test_decode_api_response_negative(self):
        """
        Negative test cases with invalid input and invalid expected and actual output.

        """

        response = client.post(
            '/shorturl/decode/',
            data=urlencode(self.payload_negative),
            content_type='application/x-www-form-urlencoded'
        )

        # Testing negative test cases
        assert response.status_code == 200
        assert response.data['status'] == 'False'

    def test_encode_api_versioning(self):
        """
        API versioning test cases.

        """

        for _version in self.supported_api_versions:
            header = {
                'HTTP_ACCEPT': 'application/json; version={}'.format(_version)
            }

            response = client.post(
                '/shorturl/decode/',
                data=urlencode(self.payload_decode_positive),
                content_type='application/x-www-form-urlencoded',
                **header
            )

            assert response.content_type == self._content_type_value + str(_version)
