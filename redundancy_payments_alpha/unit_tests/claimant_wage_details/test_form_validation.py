import unittest
from hamcrest import assert_that, is_, has_length, has_item
from claimants_user_journey.forms.claimant_wage_details import ClaimantWageDetails
from claimants_user_journey.routes import app

test_client = app.test_client()

def complete_form(data):
    with app.test_request_context('/wage-details'):
        form = ClaimantWageDetails(**data)
        return form


def complete_form_data():
    form = {
        'frequency_of_payment': 'Month',
        'gross_rate_of_pay': '18000.00',
        'frequency_of_work': 'Year',
        'number_of_hours_worked': '40',
        'bonus_or_commission': 'No',
        'overtime': 'Yes',
        'normal_days_of_work': 5
    }
    return form

class TestFormValidation(unittest.TestCase):
    def test_form_is_invalid_without_frequency_of_payment(self):
        # given
        entered_data = complete_form_data()
        del entered_data['gross_rate_of_pay']
        # when
        form = complete_form(entered_data)
        form.validate()
        # then
        assert_that(form.validate(), is_(False))

class TestFrequencyOfPayment(unittest.TestCase):
    def test_frequency_of_payment_can_be_empty(self):
        #given
        entered_data = complete_form_data()
        entered_data['frequency_of_payment'] = ''
        # when
        form = complete_form(entered_data)
        form.validate()
        # then
        assert_that(form.frequency_of_payment.errors, has_length(0))

    def test_frequency_of_payment_allows_valid_data(self):
        #given
        entered_data = complete_form_data()
        entered_data['frequency_of_payment'] = 'Year'
        # when
        form = complete_form(entered_data)
        form.validate()
        # then
        assert_that(form.frequency_of_payment.errors, has_length(0))

    def test_frequency_of_payment_does_not_allow_invalid_data(self):
        #given
        entered_data = complete_form_data()
        entered_data['frequency_of_payment'] = 'Not Valid'
        # when
        form = complete_form(entered_data)
        form.validate()
        # then
        assert_that(form.frequency_of_payment.errors, has_item('Invalid value, must be one of: Hour, Day, Week, Month, Year, .'))

class TestGrossRateOfPay(unittest.TestCase):
    def test_gross_rate_of_pay_accepts_valid_data(self):
        #given
        entered_data = complete_form_data()
        # when
        form = complete_form(entered_data)
        form.validate()
        # then
        assert_that(form.gross_rate_of_pay.errors, has_length(0))

    def test_gross_rate_of_pay_cannot_be_empty(self):
        #given
        entered_data = complete_form_data()
        entered_data['gross_rate_of_pay'] = ''
        # when
        form = complete_form(entered_data)
        form.validate()
        # then
        assert_that(form.gross_rate_of_pay.errors, has_item('This field is required.'))

    def test_gross_rate_of_pay_accepts_number_without_decimals(self):
        #given
        entered_data = complete_form_data()
        entered_data['gross_rate_of_pay'] = '200'
        # when
        form = complete_form(entered_data)
        form.validate()
        # then
        assert_that(form.gross_rate_of_pay.errors, has_length(0))

    def test_gross_rate_of_pay_accepts_number_with_decimals(self):
        #given
        entered_data = complete_form_data()
        entered_data['gross_rate_of_pay'] = '200.55'
        # when
        form = complete_form(entered_data)
        form.validate()
        # then
        assert_that(form.gross_rate_of_pay.errors, has_length(0))

    def test_gross_rate_of_pay_does_not_alpha_characters(self):
        #given
        entered_data = complete_form_data()
        entered_data['gross_rate_of_pay'] = 'Hello'
        # when
        form = complete_form(entered_data)
        form.validate()
        # then
        assert_that(form.gross_rate_of_pay.errors, has_item('Gross rate of pay must be a number e.g 100.25.'))

    def test_gross_rate_of_pay_cannot_have_more_than_eight_digits(self):
        #given
        entered_data = complete_form_data()
        entered_data['gross_rate_of_pay'] = '120120120.55'
        # when
        form = complete_form(entered_data)
        form.validate()
        # then
        assert_that(form.gross_rate_of_pay.errors, has_item('Gross rate of pay must be a number e.g 100.25.'))

    def test_gross_rate_of_pay_cannot_have_more_than_two_decimal_places(self):
        #given
        entered_data = complete_form_data()
        entered_data['gross_rate_of_pay'] = '20000.555'
        # when
        form = complete_form(entered_data)
        form.validate()
        # then
        assert_that(form.gross_rate_of_pay.errors, has_item('Gross rate of pay must be a number e.g 100.25.'))


class TestFrequencyOfWorkField(unittest.TestCase):
    def test_frequency_of_work_cannot_be_empty(self):
        #given
        entered_data = complete_form_data()
        entered_data['frequency_of_work'] = ''
        # when
        form = complete_form(entered_data)
        form.validate()
        # then
        assert_that(form.frequency_of_work.errors, has_item('This field is required.'))

    def test_frequency_of_work_allows_valid_data(self):
        #given
        entered_data = complete_form_data()
        entered_data['frequency_of_work'] = 'Year'
        # when
        form = complete_form(entered_data)
        form.validate()
        # then
        assert_that(form.frequency_of_work.errors, has_length(0))

    def test_frequency_of_work_does_not_allow_invalid_data(self):
        #given
        entered_data = complete_form_data()
        entered_data['frequency_of_work'] = 'Not Valid'
        # when
        form = complete_form(entered_data)
        form.validate()
        # then
        assert_that(form.frequency_of_work.errors, has_item('Invalid value, must be one of: Hour, Day, Week, Month, Year.'))

class TestNumberOfHoursWorked(unittest.TestCase):
    def test_number_of_hours_worked_accepts_valid_data(self):
        #given
        entered_data = complete_form_data()
        # when
        form = complete_form(entered_data)
        form.validate()
        # then
        assert_that(form.number_of_hours_worked.errors, has_length(0))

    def test_number_of_hours_worked_cannot_be_empty(self):
        #given
        entered_data = complete_form_data()
        entered_data['number_of_hours_worked'] = ''
        # when
        form = complete_form(entered_data)
        form.validate()
        # then
        assert_that(form.number_of_hours_worked.errors, has_item('This field is required.'))

    def test_number_of_hours_worked_accepts_number_without_decimals(self):
        #given
        entered_data = complete_form_data()
        entered_data['number_of_hours_worked'] = '20'
        # when
        form = complete_form(entered_data)
        form.validate()
        # then
        assert_that(form.number_of_hours_worked.errors, has_length(0))

    def test_number_of_hours_worked_accepts_number_with_decimals(self):
        #given
        entered_data = complete_form_data()
        entered_data['number_of_hours_worked'] = '20.55'
        # when
        form = complete_form(entered_data)
        form.validate()
        # then
        assert_that(form.number_of_hours_worked.errors, has_length(0))

    def test_number_of_hours_worked_does_not_alpha_characters(self):
        #given
        entered_data = complete_form_data()
        entered_data['number_of_hours_worked'] = 'Hello'
        # when
        form = complete_form(entered_data)
        form.validate()
        # then
        assert_that(form.number_of_hours_worked.errors, has_item('Number of hours you normally work must be a number e.g 40.25.'))

    def test_number_of_hours_worked_cannot_have_more_than_two_digits(self):
        #given
        entered_data = complete_form_data()
        entered_data['number_of_hours_worked'] = '120.55'
        # when
        form = complete_form(entered_data)
        form.validate()
        # then
        assert_that(form.number_of_hours_worked.errors, has_item('Number of hours you normally work must be a number e.g 40.25.'))

    def test_number_of_hours_worked_cannot_have_more_than_two_decimal_places(self):
        #given
        entered_data = complete_form_data()
        entered_data['number_of_hours_worked'] = '20.555'
        # when
        form = complete_form(entered_data)
        form.validate()
        # then
        assert_that(form.number_of_hours_worked.errors, has_item('Number of hours you normally work must be a number e.g 40.25.'))

class TestBonusOrCommission(unittest.TestCase):
    def test_bonus_or_commission_accepts_valid_data(self):
        #given
        entered_data = complete_form_data()
        # when
        form = complete_form(entered_data)
        form.validate()
        # then
        assert_that(form.bonus_or_commission.errors, has_length(0))

    def test_bonus_or_commission_has_been_selected(self):
        #given
        entered_data = complete_form_data()
        entered_data['bonus_or_commission'] = None
        # when
        form = complete_form(entered_data)
        form.validate()
        # then
        assert_that(form.bonus_or_commission.errors, has_item('Invalid value, must be one of: Yes, No.'))

class TestOvertime(unittest.TestCase):
    def test_overtime_accepts_valid_data(self):
        # given
        entered_data = complete_form_data()
        # when
        form = complete_form(entered_data)
        form.validate()
        # then
        assert_that(form.overtime.errors, has_length(0))

    def test_overtime_has_been_selected(self):
        # given
        entered_data = complete_form_data()
        entered_data['overtime'] = None
        # when
        form = complete_form(entered_data)
        form.validate()
        # then
        assert_that(form.overtime.errors, has_item("Invalid value, must be one of: Yes, No."))

class TestNormalDaysOfWork(unittest.TestCase):
    def test_normal_days_of_work_accepts_an_integer(self):
        # given
        entered_data = complete_form_data()
        # when
        form = complete_form(entered_data)
        form.validate()
        # then
        assert_that(form.normal_days_of_work.errors, has_length(0))

    def test_normal_days_of_work_will_not_accept_alpha_character(self):
        # given
        entered_data = complete_form_data()
        entered_data['normal_days_of_work'] = 'a'
        # when
        form = complete_form(entered_data)
        form.validate()
        # then
        assert_that(form.normal_days_of_work.errors, has_item('Number must be between 0 and 7.'))

    def test_normal_days_of_work_will_not_accept_more_than_one_digit(self):
        # given
        entered_data = complete_form_data()
        entered_data['normal_days_of_work'] = '12'
        # when
        form = complete_form(entered_data)
        form.validate()
        # then
        assert_that(form.normal_days_of_work.errors, has_item('Number must be between 0 and 7.'))

    #issues with the DataRequired validator as zero is falsy
#    def test_normal_days_of_work_will_accept_zero(self):
#        # given
#        entered_data = complete_form_data()
#        entered_data['normal_days_of_work'] = 0
#        # when
#        form = complete_form(entered_data)
#        form.normal_days_of_work.raw_data = form.normal_days_of_work.data
#        form.validate()
#        # then
#        assert_that(form.normal_days_of_work.errors, has_item('Number must be between 0 and 7.'))
#
