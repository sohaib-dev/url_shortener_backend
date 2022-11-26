"""
    It contains the Encode API test cases.

"""

from django.test import TestCase, Client
from urllib.parse import urlencode

client = Client()


class EncodeAPITest(TestCase):
    """
    Test module for Encode API

    """

    def setUp(self):

        self.payload_positive = {'original_url': 'google.com'}
        self.payload_negative = {'original_url': '1234'}
        self.supported_api_versions = ['1.0']
        self._content_type_value = 'application/json; version='

    def test_encode_api_response_positive(self):
        """
        Positive test cases with valid input and valid expected and actual output.

        """

        response = client.post(
            '/shorturl/encode/',
            data=urlencode(self.payload_positive),
            content_type='application/x-www-form-urlencoded'
        )

        # Testing positive test cases
        assert response.status_code == 200
        assert response.data['status'] == 'True'

    def test_encode_api_response_negative(self):
        """
        Negative test cases with invalid input and invalid expected and actual output.

        """

        response = client.post(
            '/shorturl/encode/',
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
                '/shorturl/encode/',
                data=urlencode(self.payload_positive),
                content_type='application/x-www-form-urlencoded',
                **header
            )

            assert response.content_type == self._content_type_value + str(_version)
