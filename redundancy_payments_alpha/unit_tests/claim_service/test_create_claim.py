import unittest
from hamcrest import *
from mock import patch
from claim_service.api import create_claim, _Claim

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
        assert_that(claim.discrepancies, has_entry('pay', (100,200)))
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


class TestClaimServiceIntegration(unittest.TestCase):
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

