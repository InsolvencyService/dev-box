from hamcrest import *
from mock import patch

from insolvency_practitioner_forms import routes
import form_test

def return_object():
    return object()

class TestAddingEmployeeDetails(form_test.FormTest):

    def setUp(self):
        self.app = routes.app.test_client()

    def employee_data(self, **kwargs):
        employee_data = {
            'employer_name': 'Widgets Co.',
            'employee_title': 'Other',
            'employee_title_other': 'Doctor',
            'employee_forenames': 'J',
            'employee_surname': 'Smith',
            'employee_national_insurance_class': 'z',
            'employee_national_insurance_number': 'ab123456',
            'employee_date_of_birth': '20/06/1980',
            'employee_start_date': '01/01/1980',
            'employee_date_of_notice': '01/01/1990',
            'employee_end_date': '05/01/1990',
            'employee_basic_weekly_pay': '600',
            'employee_weekly_pay_day': 'monday',
            'employee_owed_wages_from': '01/12/1989',
            'employee_owed_wages_to': '05/01/1990',
            'employee_owed_wages_in_arrears': '1200.50',
            'employee_owed_wages_in_arrears_type': 'wages',
            'employee_holiday_year_start_date': '01/01/1990',
            'employee_holiday_owed': '5.5',
            'employee_unpaid_holiday_from': '01/01/1990',
            'employee_unpaid_holiday_to': '01/01/1990'
        }
        employee_data.update(kwargs)
        return employee_data

    @patch('insolvency_practitioner_forms.routes.get_storage_service')
    def test_posting_complete_employee_details_redirects_to_employee_added_page(self, mocked_storage_factory):
        response = self.submit_form(
            self.app,
            '/create-employee-record/employee-details/',
            self.employee_data()
        )
        assert_that(response.status_code, is_(302))
        assert_that(response.headers, has_entry('Location', contains_string('/create-employee-record/employee-added/')))

    def test_posting_empty_employee_details_keeps_submitter_on_form_page(self):
        response = self.submit_form(
            self.app,
            '/create-employee-record/employee-details/',
            {}
        )
        assert_that(response.status_code, is_(200))

