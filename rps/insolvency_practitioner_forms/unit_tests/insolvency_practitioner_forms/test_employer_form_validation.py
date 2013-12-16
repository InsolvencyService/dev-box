import form_test

from hamcrest import *

from insolvency_practitioner_forms.forms.employer_details_form import EmployerDetailsForm
from insolvency_practitioner_forms import routes

class TestFormValidation(form_test.FormTest):
    def test_date_validation(self):
        # given
        form = self.create_form(
            routes.app,
            'create-insolvency-case/employer-details/',
            EmployerDetailsForm,
            date_of_insolvency='wibble'
        )
        
        # when
        form.validate()

        # then
        assert_that(
            form.date_of_insolvency.errors,
            has_item('Date must be in the format dd/mm/yyyy.')
        )

    def test_company_number_validation(self):
        # given
        form = self.create_form(
            routes.app,
            'create-insolvency-case/employer-details/',
            EmployerDetailsForm,
            company_number='wibble'
        )
        
        # when
        form.validate()

        # then
        assert_that(
            form.company_number.errors,
            has_item('Company number must be a number.')
        )

    def test_insolvency_practitioner_registration_validation(self):
        # given
        form = self.create_form(
            routes.app,
            'create-insolvency-case/employer-details/',
            EmployerDetailsForm,
            insolvency_practitioner_registration='wibble'
        )
        
        # when
        form.validate()

        # then
        assert_that(
            form.insolvency_practitioner_registration.errors,
            has_item('Insolvency Practitioner Registration must be a number.')
        )

    def test_insolvency_type_validation(self):
        # given
        form = self.create_form(
            routes.app,
            'create-insolvency-case/employer-details/',
            EmployerDetailsForm,
            type_of_insolvency='wibble'
        )
        
        # when
        form.validate()

        # then
        assert_that(
            form.type_of_insolvency.errors,
            has_item('Not a valid choice')
        )

    def test_field_lengths(self):
       # given 
        form = self.create_form(
            routes.app,
            'create-insolvency-case/employer-details/',
            EmployerDetailsForm,
            company_name='a'*61, 
            company_number='1'*11,
            nature_of_business='a'*61,
            insolvency_practitioner_name='a'*31,
            insolvency_practitioner_registration='1'*16,
            insolvency_practitioner_firm='a'*31,
            address_line_1='a'*8,
            address_line_2='a'*23,
            address_line_3='a'*31,
            town_or_city='a'*31,
            postcode='a'*9,
            country='a'*31,
            email_address='a'*61,
            telephone_number='a'*41
        )

        # when
        form.validate()

        # then
        assert_that(form.company_name.errors, has_item(contains_string('Field cannot be longer than'))) 
        assert_that(form.company_number.errors, has_item(contains_string('Field cannot be longer than')))
        assert_that(form.nature_of_business.errors, has_item(contains_string('Field cannot be longer than')))
        assert_that(form.insolvency_practitioner_name.errors, has_item(contains_string('Field cannot be longer than')))
        assert_that(form.insolvency_practitioner_registration.errors, has_item(contains_string('Field cannot be longer than')))
        assert_that(form.insolvency_practitioner_firm.errors, has_item(contains_string('Field cannot be longer than')))
        assert_that(form.address_line_1.errors, has_item(contains_string('Field cannot be longer than')))
        assert_that(form.address_line_2.errors, has_item(contains_string('Field cannot be longer than')))
        assert_that(form.address_line_3.errors, has_item(contains_string('Field cannot be longer than')))
        assert_that(form.town_or_city.errors, has_item(contains_string('Field cannot be longer than')))
        assert_that(form.postcode.errors, has_item(contains_string('Field cannot be longer than')))
        assert_that(form.country.errors, has_item(contains_string('Field cannot be longer than')))
        assert_that(form.email_address.errors, has_item(contains_string('Field cannot be longer than')))
        assert_that(form.telephone_number.errors, has_item(contains_string('Field cannot be longer than')))

