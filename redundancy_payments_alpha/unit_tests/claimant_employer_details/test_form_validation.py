from datetime import datetime
import unittest
from hamcrest import assert_that, is_, has_length, has_item
from claimants_user_journey.forms.employment_details import EmploymentDetails
from claimants_user_journey.routes import app

test_client = app.test_client()


def complete_form(data):
    with app.test_request_context('/employment-details'):
        form = EmploymentDetails(**data)
        return form


def complete_form_data():
    form = {
        'job_title': 'Job Title',
        'type_of_worker': 'employed',
        'start_date': {
            'day': '20',
            'month': '2',
            'year': '1985'
        },
        'end_date': {
            'day': '21',
            'month': '3',
            'year': '1999'
        }
    }
    return form

class TestFormValidation(unittest.TestCase):
    def test_form_is_invalid_without_job_title(self):
        # given
        entered_data = complete_form_data()
        del entered_data['job_title']
        # when
        form = complete_form(entered_data)
        form.validate()
        # then
        assert_that(form.validate(), is_(False))


class TestJobTitleValidation(unittest.TestCase):
    def test_job_title_field_allows_strings(self):
        # given
        entered_data = complete_form_data()
        # when
        form = complete_form(entered_data)
        form.validate()
        # then
        assert_that(form.job_title.errors, has_length(0))

    def test_job_title_field_can_be_no_longer_than_30_characters(self):
        # given
        entered_data = complete_form_data()
        entered_data['job_title'] = 'a' * 31
        # when
        form = complete_form(entered_data)
        form.validate()
        # then
        assert_that(form.job_title.errors, has_item('Field cannot be longer than 30 characters.'))

class TestCategoryOfWorker(unittest.TestCase):
    def test_type_of_worker_field_allows_a_valid_selection(self):
        # given
        entered_data = complete_form_data()
        # when
        form = complete_form(entered_data)
        form.validate()
        # then
        assert_that(form.type_of_worker.errors, has_length(0))

    def test_type_of_worker_field_will_not_allow_invalid_selection(self):
        # given
        entered_data = complete_form_data()
        entered_data['type_of_worker'] = 'not a valid choice'
        # when
        form = complete_form(entered_data)
        form.validate()
        # then
        assert_that(form.type_of_worker.errors, has_item('Not a valid choice'))

class TestStartDate(unittest.TestCase):
    def test_start_date_field_allows_a_valid_date(self):
        # given
        entered_data = complete_form_data()
        # when
        form = complete_form(entered_data)
        form.validate()
        # then
        assert_that(form.start_date.errors, has_length(0))

    def test_start_date_field_does_not_display_the_int_parsing_error_when_letters_are_used_in_place_of_numbers(self):
        # given
        entered_date = complete_form_data()
        entered_date['start_date'] = {
            'day': '21',
            'month': '3',
            'year': 'cccc'
        }
        # when
        form = complete_form(entered_date)
        form.validate()
        # then
        assert_that(form.start_date.errors, has_item("Date must be in the format dd/mm/yyyy.") )
        assert_that(form.start_date.errors, has_length(1))

    def test_start_date_field_is_invalid_with_date_greater_than_today(self):
        # given
        entered_date = complete_form_data()
        entered_date['start_date'] = {
            'day': '30',
            'month': '1',
            'year': '3000'
        }
        # when
        form = complete_form(entered_date)
        form.validate()
        # then
        assert_that(form.start_date.errors, has_item("Date must be greater than or equal to 1900 and not in the future.") )


class TestEndDate(unittest.TestCase):
    def test_end_date_field_allows_a_valid_date(self):
        # given
        entered_data = complete_form_data()
        # when
        form = complete_form(entered_data)
        form.validate()
        # then
        assert_that(form.end_date.errors, has_length(0))

    def test_end_date_field_does_not_display_the_int_parsing_error_when_letters_are_used_in_place_of_numbers(self):
        # given
        entered_date = complete_form_data()
        entered_date['end_date'] = {
            'day': '21',
            'month': '3',
            'year': 'cccc'
        }
        # when
        form = complete_form(entered_date)
        form.validate()
        # then
        assert_that(form.end_date.errors, has_item("Date must be in the format dd/mm/yyyy.") )
        assert_that(form.end_date.errors, has_length(1))

    def test_start_date_field_is_invalid_with_date_greater_than_today(self):
        # given
        entered_date = complete_form_data()
        entered_date['end_date'] = {
            'day': '21',
            'month': '3',
            'year': '3000'
        }
        # when
        form = complete_form(entered_date)
        form.validate()
        # then
        assert_that(form.end_date.errors, has_item("Date must be greater than or equal to 1900 and not in the future.") )

