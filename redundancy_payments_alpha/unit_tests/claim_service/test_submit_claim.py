import unittest
from mock import patch
from claim_service.api import submit


class TestSubmitClaim(unittest.TestCase):
    @patch('claim_service.api.cabinet_api')
    def test_claim_submission(self, mock_cabinet):
        claim_id = 123456
        submit(123456)
        mock_cabinet.submit_claim.assert_called_with(claim_id)
