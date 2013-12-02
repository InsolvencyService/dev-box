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

    def test_extracts_values_to_compare_for_gross_amount_owed(self):
        claim = (
            {'gross_amount_owed': 'wibble'},
            {'employee_owed_wages_in_arrears': 'bannana'}
        )

        values = comparable_values(claim)

        assert_that(values, has_entry('gross_amount_owed', ('wibble', 'bannana')))

    def test_extracts_multiple_values_to_compare(self):
        claim = (
            {'gross_amount_owed': 'wibble',
             'gross_rate_of_pay': 'x'},
            {'employee_owed_wages_in_arrears': 'bannana',
             'employee_basic_weekly_pay': 'y'}
        )

        values = comparable_values(claim)

        assert_that(values, has_entry('gross_amount_owed', ('wibble', 'bannana')))
        assert_that(values, has_entry('gross_rate_of_pay', ('x', 'y')))

    def handles_empty_claim(self):
        claim = ()
        values = comparable_values(claim)
        assert_that(values, is_({}))

