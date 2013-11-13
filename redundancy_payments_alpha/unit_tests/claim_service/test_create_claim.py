import unittest
from hamcrest import *
from mock import patch
from claim_service.api import create_claim, _Claim


class TestCreateClaim(unittest.TestCase):
    def test_returns_none_if_claimant_does_not_match_any_employee_records(self):
        claimant_information = {
            'nino': 'AB333333C'
        }

        claim = create_claim(claimant_information)
        assert_that(claim, is_(None))

    def test_returns_claim_if_claimant_matches_employee_record(self):
        claimant_information = {
            'nino': 'AB333333D'
        }

        claim = create_claim(claimant_information)
        assert_that(claim, is_not(None))


class TestClaim(unittest.TestCase):
    def test_(self):
        claimant_information = {
            'nino': 'x',
            'pay': 100
        }

        employee_record = {
            'nino': 'x',
            'pay': 200
        }

        claim = _Claim(claimant_information, employee_record)

        assert_that(claim.discrepancies, has_length(1))

