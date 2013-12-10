import unittest

from hamcrest import assert_that, is_

from claimants_user_journey import calculators as calc 


class TestCalculators(unittest.TestCase):
    def test_yearly_to_weekly_gross_rate_of_pay(self):
        details = {'gross_pay': '25000', 'period': 'year'}
        gross_pay = calc.yearly_to_weekly_gross_rate_of_pay(details)
        assert_that(gross_pay, is_('479.45'))

