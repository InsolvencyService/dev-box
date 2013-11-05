import unittest
from hamcrest import assert_that, is_, has_length, has_item
from ...claimants_user_journey.forms.wages_owed import WagesOwed
from ...claimants_user_journey.routes import app

test_client = app.test_client()


def complete_form(data):
    with app.test_request_context('/wages-owed'):
        form = WagesOwed(**data)
        return form


def complete_form_data():
    form = {
        'owed': 'Y',
        'wage_owed_from': '20/02/1985',
        'wage_owed_to': '21/03/1999',
        'number_of_days_owed': '1',
        'gross_amount_owed': '1.50'
    }
    return form

class TestFormValidation(unittest.TestCase):
    def test_form_is_invalid_without_owed(self):
        # given
        entered_data = complete_form_data()
        del entered_data['owed']
        # when
        form = complete_form(entered_data)
        form.validate()
        # then
        assert_that(form.validate(), is_(False))


class TestOwedValidation(unittest.TestCase):
    def test_owed_field_allows_valid_selection(self):
        # given
        entered_data = complete_form_data()
        # when
        form = complete_form(entered_data)
        form.validate()
        # then
        assert_that(form.owed.errors, has_length(0))

class TestWageOwedFrom(unittest.TestCase):
    def test_wage_owed_from_field_allows_a_valid_date(self):
        # given
        entered_data = complete_form_data()
        # when
        form = complete_form(entered_data)
        form.validate()
        # then
        assert_that(form.wage_owed_from.errors, has_length(0))

    def test_wage_owed_from_field_does_not_allow_incorrectly_formatted_date(self):
        # given
        entered_date = complete_form_data()
        entered_date['wage_owed_from'] = '01//01/1990'
        # when
        form = complete_form(entered_date)
        form.validate()
        # then
        assert_that(form.wage_owed_from.errors, has_item("Date must be in the format dd/mm/yyyy.") )

class TestWageOwedTo(unittest.TestCase):
    def test_wage_owed_to_field_allows_a_valid_date(self):
        # given
        entered_data = complete_form_data()
        # when
        form = complete_form(entered_data)
        form.validate()
        # then
        assert_that(form.wage_owed_to.errors, has_length(0))

    def test_wage_owed_to_field_does_not_allow_incorrectly_formatted_date(self):
        # given
        entered_date = complete_form_data()
        entered_date['wage_owed_to'] = '01//01/1990'
        # when
        form = complete_form(entered_date)
        form.validate()
        # then
        assert_that(form.wage_owed_to.errors, has_item("Date must be in the format dd/mm/yyyy.") )

class TestNumberOfDaysOwed(unittest.TestCase):
    def test_number_of_days_owed_field_allows_valid_integer(self):
        # given
        entered_data = complete_form_data()
        # when
        form = complete_form(entered_data)
        form.validate()
        # then
        assert_that(form.number_of_days_owed.errors, has_length(0))

    def test_number_of_days_owed_field_does_not_allow_non_integer(self):
        # given
        entered_days_owed = complete_form_data()
        entered_days_owed['number_of_days_owed'] = 'x'
        # when
        form = complete_form(entered_days_owed)
        form.validate()
        # then
        assert_that(form.number_of_days_owed.errors, has_item("Number of days owed must be numeric.") )

class TestGrossAmountOwed(unittest.TestCase):
    def test_gross_amount_owed_field_allows_valid_decimal(self):
        # given
        entered_data = complete_form_data()
        # when
        form = complete_form(entered_data)
        form.validate()
        # then
        assert_that(form.gross_amount_owed.errors, has_length(0))

    def test_gross_amount_owed_field_does_not_allow_non_decimal(self):
        # given
        entered_gross_amount_owed = complete_form_data()
        entered_gross_amount_owed['gross_amount_owed'] = '1.x'
        # when
        form = complete_form(entered_gross_amount_owed)
        form.validate()
        # then
        assert_that(form.gross_amount_owed.errors, has_item("Gross amount owed must be numeric.") )
