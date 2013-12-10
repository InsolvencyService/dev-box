import unittest
from datetime import date
from hamcrest import assert_that, is_
from claimants_user_journey.forms.validators import convert_string_to_date

class TestStringToDate(unittest.TestCase):
    def test_string_in_dd_mm_yyyy_gets_converted_to_date(self):
        # given
        a_string = '01/02/1984'
        # when
        parsed_date = convert_string_to_date(a_string)
        # then
        assert_that(parsed_date, is_(date(1984, 2, 1)))

    def test_raises_exception_if_string_has_too_few_strings(self):
        a_string = 'not a date'
        self.assertRaises(SyntaxError, convert_string_to_date, a_string)
