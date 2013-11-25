from decimal import Decimal
import unittest
from datetime import date

from hamcrest import *
from mock import patch

from claim_service.api import add_details_to_claim, create_claim_2


class TestCreateClaim2(unittest.TestCase):
    @patch('claim_service.api.cabinet_api')
    def test_claims_get_created_with_matching_records(self, mock_cabinet):
        mock_cabinet.employee_via_nino.return_value = {'foo':'bar'}
        mock_cabinet.add_claim.return_value = 1
        personal_details = {
            'nino': 'AB012345Z'
        }
        claim_id = create_claim_2(personal_details)
        mock_cabinet.add_claim.assert_called_with(personal_details, {'foo':'bar'})

    @patch('claim_service.api.cabinet_api')
    def test_claims_dont_get_created_if_no_record_is_found(self, mock_cabinet):
        mock_cabinet.employee_via_nino.return_value = None
        personal_details = {
            'nino': 'AB012345Z'
        }
        claim_id = create_claim_2(personal_details)
        assert_that(claim_id, is_(None))


class TestAddDetailsToClaim(unittest.TestCase):
    @patch('claim_service.api.cabinet_api')
    def test_add_details_to_claim(self, mock_cabinet):
        mock_cabinet.get_claim.return_value = ({'a': '_'},{'b': '_'})
        claim_id = 12
        claimant_details = {'a': 'b'}
        claim = add_details_to_claim(claim_id, claimant_details)
        mock_cabinet.update_claim.assert_called_with(
            claim_id,
            claimant_information=claimant_details
        )
