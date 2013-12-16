import unittest
from hamcrest import assert_that, is_, has_length, has_item
from claimants_user_journey.forms.holiday_pay import HolidayPay
from claimants_user_journey.routes import app

test_client = app.test_client()

def complete_form(data):
    with app.test_request_context('/holiday-pay'):
        form = HolidayPay(**data)
        return form


def complete_form_data():
    form = {
        'csrf_token': 'a',
        'holiday_owed': 'Yes',
        'holiday_start_date': '01/01/2001',
        'number_of_holiday_days_entitled': '21',
        'days_carried_over': '4',
        'days_taken': '10',
        'days_owed': '15',
        'holiday_taken_from':'01/02/2001',
        'holiday_taken_to':'11/02/2001',
        'number_of_days_pay_owed':'15'
    }
    return form

class TestFormValidation(unittest.TestCase):
    def test_form_accepts_valid_input(self):
        # given
        entered_data = complete_form_data()
        # when
        form = complete_form(entered_data)
        form.validate()

        # then
        assert_that(form.days_carried_over.errors, has_length(0))
        assert_that(form.holiday_owed.errors, has_length(0))
        assert_that(form.holiday_start_date.errors, has_length(0))
        assert_that(form.number_of_holiday_days_entitled.errors, has_length(0))
        assert_that(form.days_taken.errors, has_length(0))
        assert_that(form.days_owed.errors, has_length(0))
        assert_that(form.holiday_taken_from.errors, has_length(0))
        assert_that(form.holiday_taken_to.errors, has_length(0))
        assert_that(form.number_of_days_pay_owed.errors, has_length(0))
