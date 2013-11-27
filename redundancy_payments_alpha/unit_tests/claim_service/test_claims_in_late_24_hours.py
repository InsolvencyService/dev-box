from datetime import datetime
import unittest
from hamcrest import assert_that, has_length
from mock import patch

import claim_service.api as claim_api


class TestClaimsSubmittedInLast24Hours(unittest.TestCase):
    @patch('claim_service.api.cabinet_api')
    @patch('claim_service.api._current_time')
    def test_we_get_24_hours_of_claims(self, mock_time, mock_cabinet):
        mock_time.return_value = datetime(1990, 1, 7)

        claims = claim_api.claims_submitted_in_last_24_hours()

        mock_cabinet.get_claims_submitted_between.assert_called_with(
            start=datetime(1990, 1, 6),
            end=datetime(1990, 1, 7)
        )
