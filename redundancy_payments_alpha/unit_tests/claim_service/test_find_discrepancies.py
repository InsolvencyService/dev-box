import unittest

from mock import patch
from hamcrest import assert_that, has_length, has_entry, is_

from claim_service.api import find_discrepancies, has_discrepancies

class TestFindDiscrepancies(unittest.TestCase):
    @patch('claim_service.api.cabinet_api')
    def test_returns_values_of_discrepant_wage_details(self, mock_cabinet):
        mock_cabinet.get_claim.return_value = (
            {'gross_rate_of_pay': '600'},
            {'employee_basic_weekly_pay': '650'}
        )
        claim_id = 1

        discrepancies = find_discrepancies(claim_id)
        assert_that(discrepancies, has_length(1))
        assert_that(discrepancies, has_entry('gross_rate_of_pay', ('600','650')))


    @patch('claim_service.api.cabinet_api')
    def test_returns_no_discrepancies_for_matching_data(self, mock_cabinet):
        mock_cabinet.get_claim.return_value = (
            {'gross_rate_of_pay': '650'},
            {'employee_basic_weekly_pay': '650'}
        )
        claim_id = 1

        discrepancies = find_discrepancies(claim_id)
        assert_that(discrepancies, has_length(0))
    
    @patch('claim_service.api.cabinet_api')
    def test_returns_does_not_exception_with_missing_gross_rate_of_pay(self, mock_cabinet):
        mock_cabinet.get_claim.return_value = (
            {'glross_rate_of_pay': '650'},
            {'employee_basic_weekly_pay': '650'}
        )
        claim_id = 1
        discrepancies = find_discrepancies(claim_id)

    @patch('claim_service.api.cabinet_api')
    def test_should_be_able_to_say_if_discrepancies(self, mock_cabinet):
        mock_cabinet.get_claim.return_value = (
            {'gross_rate_of_pay': '650'},
            {'employee_basic_weekly_pay': '651'}
        )
        assert_that(has_discrepancies(1), is_(True))

    @patch('claim_service.api.cabinet_api')
    def test_should_be_able_to_say_no_discrepancies(self, mock_cabinet):
        mock_cabinet.get_claim.return_value = (
            {'gross_rate_of_pay': '650'},
            {'employee_basic_weekly_pay': '650'}
        )
        assert_that(has_discrepancies(1), is_(False))
