import unittest
import json

from hamcrest import is_, assert_that

from birmingham_cabinet.routes import app

class TestStoringContactDetails(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestStoringContactDetails, self).__init__(*args, **kwargs)
        self.test_client = app.test_client()

    def claimant(self):
        return {
            'forenames': 'Donald',
            'surname': 'Duck',
            'title': 'Mr',
            'other': '',
            'building_number': '5',
            'street': 'street name',
            'district': 'district name',
            'town_or_city': 'Duckburg',
            'county': 'county name',
            'postcode': 'A1 2BC',
            'email': 'donald.duck@duckburg.com',
            'telephone_number': '12345 123456',
            'nino': 'AA112233B',
            'date_of_birth': '01/01/1900'
        }

    def test_should_store_contact_details(self):
        claimant = self.claimant()
        json_headers = [("Content-Type", "application/json")]
        url = "/claimant-contact-details/{nino}".format(nino=claimant["nino"])
        response = self.test_client.post(
            url,
            data=json.dumps(claimant),
            headers=json_headers)
        assert_that(response.status_code, is_(201))

        response = self.test_client.get(url)
        assert_that(response.status_code, is_(200))
        assert_that(json.loads(response.data), is_(claimant))