import unittest
from hamcrest import *
from mock import patch
from claim_service.api import create_claim

class TestCreateClaim(unittest.TestCase):
    def test_returns_none_if_claimant_does_not_match_any_employee_records(self):
        claimant_information = {
            'nino': 'AB333333C'
        }

        claim = create_claim(claimant_information)
        assert_that(claim, is_(None))

