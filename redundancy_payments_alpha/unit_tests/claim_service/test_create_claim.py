from decimal import Decimal
import unittest
from hamcrest import *
from mock import patch
from claim_service.api import create_claim, _Claim, create_claim_2

class TestCreateClaim(unittest.TestCase):
    @patch('claim_service.api.employee_via_nino')
    def test_returns_none_if_claimant_does_not_match_any_employee_records(self, mock_employee_via_nino):
        mock_employee_via_nino.return_value = None

        claimant_information = {
            'nino': 'AB333333C'
        }

        claim = create_claim(claimant_information)
        assert_that(claim, is_(None))

    @patch('claim_service.api.employee_via_nino')
    def test_returns_claim_if_claimant_matches_employee_record(self, mock_employee_via_nino):
        mock_employee_via_nino.return_value = {'foo':'bar'}

        claimant_information = {
            'nino': 'AB333333D'
        }

        claim = create_claim(claimant_information)
        assert_that(claim, is_not(None))


class TestCreateClaim2(unittest.TestCase):
    @patch('claim_service.api.add_claim')
    @patch('claim_service.api.employee_via_nino')
    def test_claims_get_created_with_matching_records(self, mock_employee, mock_add_claim):
        mock_employee.return_value = 'foo'
        mock_add_claim.return_value = 1
        personal_details = {
            'nino': 'AB012345Z'
        }
        claim_id = create_claim_2(personal_details)
        mock_add_claim.assert_called_with(personal_details, 'foo')

    @patch('claim_service.api.employee_via_nino')
    def test_claims_dont_get_created_if_no_record_is_found(self, mock_employee):
        mock_employee.return_value = None 
        personal_details = {
            'nino': 'AB012345Z'
        }
        claim_id = create_claim_2(personal_details)
        assert_that(claim_id, is_(None))

class TestClaim(unittest.TestCase):
    def test_discrepacies_are_detected(self):
        claimant_information = {
            'nino': 'x',
            'pay': 100,
            'foo': 'bar',
            'tennis': 'bar'
        }

        employee_record = {
            'nino': 'x',
            'pay': 200,
            'foo': 'zap',
            'tennis': 'bar'
        }

        claim = _Claim(claimant_information, employee_record)

        assert_that(claim.discrepancies, has_length(2))
        assert_that(claim.discrepancies, has_entry('pay', ('100','200')))
        assert_that(claim.discrepancies, has_entry('foo', ('bar','zap')))

    def test_only_detects_discrepancies_where_value_is_given_by_both(self):
        claimant_information = {
            'nino': 'x',
            'tennis': 'bar'
        }

        employee_record = {
            'nino': 'x',
            'rugby': 'wombat'
        }

        claim = _Claim(claimant_information, employee_record)

        assert_that(claim.discrepancies, has_length(0))

    def test_wages_details_are_mapped_to_employee_details(self):
        claimant_information = {
            'gross_rate_of_pay': '600'
        }

        employee_record = {
            'employee_basic_weekly_pay': '650'
        }

        claim = _Claim(claimant_information, employee_record)

        assert_that(claim.discrepancies,
                    has_entry('gross_rate_of_pay', ('600', '650')))

    def test_everything_is_compared_as_strings_until_we_make_it_better(self):
        claimant_information = {
            'wombat': '7',
            'foobar': '0.5',
            'wibble': '6'
        }

        employee_record = {
            'wombat': 7,
            'foobar': Decimal('0.5'),
            'wibble': 5
        }

        claim = _Claim(claimant_information, employee_record)

        assert_that(claim.discrepancies, has_length(1))
        assert_that(claim.discrepancies,
                    has_entry('wibble', ('6', '5')))


class TestClaimServiceEdgeToEdge(unittest.TestCase):
    @patch('claim_service.api.employee_via_nino')
    def test_claim_service_integration(self, mock_employee_via_nino):
        mock_employee_via_nino.return_value = {
            'nino': 'x',
            'cats': 'dogs'
        }

        claimant_information = {
            'nino': 'x',
            'cats': 'kittens'
        }

        claim = create_claim(claimant_information)

        assert_that(claim.discrepancies, has_entry('cats', ('kittens','dogs')))
