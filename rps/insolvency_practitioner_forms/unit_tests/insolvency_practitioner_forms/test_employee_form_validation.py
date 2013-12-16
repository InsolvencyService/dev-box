from hamcrest import *
from insolvency_practitioner_forms import routes
from insolvency_practitioner_forms.forms.employee_details_form import EmployeeDetailsForm
import form_test


class TestEmployeeFormValidation(form_test.FormTest):
    def test_other_must_have_a_value_if_title_is_other(self):
        form = self.create_form(
            app = routes.app,
            url = '/create-employee-record/employee-added/',
            form_class = EmployeeDetailsForm, 
            employee_title='Other',
            employee_title_other=''
        )
        form.validate()
        assert_that(form.employee_title_other.errors, has_item('A title must be provided if other is selected.'))

    def test_other_can_be_empty_if_title_is_selected(self):
        form = self.create_form(
            app = routes.app,
            url = '/create-employee-record/employee-added/',
            form_class = EmployeeDetailsForm, 
            employee_title='mr',
            employee_title_other=''
        )
        form.validate()
        assert_that(form.employee_title_other.errors, has_length(0))

    def test_national_insurance_class_must_be_a_single_letter(self):
        form = self.create_form(
            app = routes.app,
            url = '/create-employee-record/employee-added/',
            form_class = EmployeeDetailsForm, 
            employee_national_insurance_class='1'
        )
        form.validate()
        assert_that(form.employee_national_insurance_class.errors, has_item('foo'))

    def test_national_insurance_class_must_be_a_single_letter(self):
        form = self.create_form(
            app = routes.app,
            url = '/create-employee-record/employee-added/',
            form_class = EmployeeDetailsForm, 
            employee_national_insurance_class='a'
        )
        form.validate()
        assert_that(form.employee_national_insurance_class.errors, has_length(0))
    
    def test_length_validations(self):
        form = self.create_form(
            app = routes.app,
            url = '/create-employee-record/employee-added/',
            form_class = EmployeeDetailsForm, 
            employer_name='a'*61,
            employee_title='Other',
            employee_title_other='a'*16,
            employee_forenames='a'*41,
            employee_surname='a'*61
        )
        form.validate()
        assert_that(form.employer_name.errors, has_item(contains_string('Field cannot be longer than')))
        assert_that(form.employee_title_other.errors, has_item(contains_string('Field cannot be longer than')))
        assert_that(form.employee_forenames.errors, has_item(contains_string('Field cannot be longer than')))
        assert_that(form.employee_surname.errors, has_item(contains_string('Field cannot be longer than')))

