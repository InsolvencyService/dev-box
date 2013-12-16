import form_test
from insolvency_practitioner_forms import routes
from hamcrest import *
from BeautifulSoup import BeautifulSoup

class TestCreatingAnInsolvencyCase(form_test.FormTest):
    def setUp(self):
        self.app = routes.app.test_client()

    def form_data(self, **kwargs): 
        form_data = {
            'company_name': 'Self Pres 12#',
            'company_number': '98998987',
            'nature_of_business': 'Stealing gold from Italian banks',
            'date_of_insolvency': '01/05/2013',
            'type_of_insolvency': 'compulsory_liquidation',
            'insolvency_practitioner_name': 'Tywin Lannster',
            'insolvency_practitioner_registration': '9888',
            'insolvency_practitioner_firm':'House Lannister',
            'address_line_1':'269a',
            'address_line_2':'Winterfell',
            'address_line_3':'Summerhasdied St',
            'town_or_city':'Birmingham',
            'postcode':'B4 6FD',
            'country':'England',
            'email_address':'tywin.lannister@hotmail.co.uk',
            'telephone_number':'07537345763'
        }
        form_data.update(kwargs)
        return form_data

    def test_posting_complete_form_redirects_to_okay_page(self):
        response = self.submit_form(
            self.app,
            '/create-insolvency-case/employer-details/',
            self.form_data()
        )
        assert_that(response.status_code, is_(302))

    def test_posting_empty_form_remains_on_submission_page(self):
        response = self.submit_form(
            self.app,
            '/create-insolvency-case/employer-details/',
            {}
        )
        assert_that(response.status_code, is_(200))

    def test_company_number_is_optional(self):
        response = self.submit_form(
            self.app,
            '/create-insolvency-case/employer-details/',
            self.form_data(company_number='')
        )
        assert_that(response.status_code, is_(302))

    def test_address_line_3_is_optional(self):
        response = self.submit_form(
            self.app,
            '/create-insolvency-case/employer-details/',
            self.form_data(address_line_3='')
        )
        assert_that(response.status_code, is_(302))

