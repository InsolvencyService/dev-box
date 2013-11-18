import unittest

from hamcrest import assert_that, has_entry, is_

from claim_service.discrepancies import comparable_values

class TestComparableValues(unittest.TestCase):
    def test_extracts_values_to_compare_for_wage_details(self):
        claim = (
            {'gross_rate_of_pay': '_'},
            {'employee_basic_weekly_pay': '_'}
        )

        values = comparable_values(claim)

        assert_that(values, has_entry('gross_rate_of_pay', ('_','_')))

    def handles_empty_claim(self):
        claim = ()
        values = comparable_values(claim)
        assert_that(values, is_({}))

