import unittest

from BeautifulSoup import BeautifulSoup
from hamcrest import assert_that, has_entry, contains_string
from mock import patch

from claimants_user_journey.routes import app


def _fill_out_form(client, url, session=None, **kwargs):
    response = client.get(url)
    page = BeautifulSoup(response.data)
    csrf_token = page.find('input', id='csrf_token')['value']
    kwargs['csrf_token'] = csrf_token
    r = None
    with client as c:
        with c.session_transaction() as s:
            if session:
                s.update(session)
        r = c.post(url, data=kwargs)
    return r


class TestMatchingClaiamantToEmployeeRecords(unittest.TestCase):

    form_data = {
        'forenames':'Donald',
        'surname':'Duck',
        'title':'Mr',
        'other':'',
        'building_number':'5',
        'street':'street name',
        'district':'district name',
        'town_or_city':'Duckburg',
        'county':'county name',
        'postcode':'A1 2BC',
        'email':'donald.duck@duckburg.com',
        'telephone_number':'12345 123456',
        'nino':'AA112233B',
        'date_of_birth-day': '1',
        'date_of_birth-month': '2',
        'date_of_birth-year': '1983'
    }

    def setUp(self):
        self.client = app.test_client()


    @patch('claimants_user_journey.routes.claim_service')
    def test_claimant_is_sent_to_next_stage_if_matched(self, mock_claim_service):
        mock_claim_service.create_claim_2.return_value = 5
        response = _fill_out_form(
            self.client,
            '/claim-redundancy-payment/personal-details/',
            **self.form_data
        )
        assert_that(response.headers, has_entry('Location',
            contains_string('/claim-redundancy-payment/employment-details/')))

    @patch('claimants_user_journey.routes.claim_service')
    def test_claimant_is_sent_to_call_your_ip_if_not_matched(self, mock_claim_service):
        mock_claim_service.create_claim_2.return_value = None
        response = _fill_out_form(
            self.client,
            '/claim-redundancy-payment/personal-details/',
            **self.form_data
        )
        assert_that(response.headers, has_entry('Location',
            contains_string('/claim-redundancy-payment/call-your-ip/')))


class TestFindingDiscrepanciesInPersonalDetails(unittest.TestCase):
    
    form_data = {
        'frequency_of_payment': 'Week',
        'gross_rate_of_pay': '18000.00',
        'number_of_hours_worked': '40',
        'bonus_or_commission': 'No',
        'overtime': 'Yes',
        'normal_days_of_work': '5'
    }

    def setUp(self):
        self.client = app.test_client()

    @patch('claimants_user_journey.routes.claim_service')
    def test_claimant_is_sent_to_discrepancies_page_when_discrepancies_found(self, mock_claim_service):
        mock_claim_service.find_discrepancies.return_value = ['this should be a list of discrepancies']
        response = _fill_out_form(
            self.client,
            '/claim-redundancy-payment/wage-details/',
            session={'claim_id': 15},
            **self.form_data
        )

        assert_that(response.headers, has_entry(
            'Location',
            contains_string('/claim-redundancy-payment/wage-details/discrepancies/')
        ))

    @patch('claimants_user_journey.routes.claim_service')
    def test_claimant_skips_discrepancies_page_when_there_are_no_discrepancies(self, mock_claim_service):
        mock_claim_service.find_discrepancies.return_value = []
        response = _fill_out_form(
            self.client,
            '/claim-redundancy-payment/wage-details/',
            session={'claim_id': 15},
            **self.form_data
        )

        assert_that(response.headers, has_entry(
            'Location',
            contains_string('/claim-redundancy-payment/holiday-pay/')
        ))
