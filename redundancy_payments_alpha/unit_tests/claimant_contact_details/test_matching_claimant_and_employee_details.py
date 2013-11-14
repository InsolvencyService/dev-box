import unittest

from BeautifulSoup import BeautifulSoup
from hamcrest import (
    assert_that,
    contains_string,
    is_
)
from mock import patch

from claimants_user_journey import routes

class TestMatchingClaimantAndEmployeeDetails(unittest.TestCase):
    @patch("claimants_user_journey.routes.employee_via_nino")
    def test_claimant_is_sent_to_nino_not_found_page(self, employee_via_nino):
        employee_via_nino.return_value = {"first_name": "John"}

        test_app = routes.app.test_client()
        response = test_app.get('/claim-redundancy-payment/employee-records/?nino=AB999999C')
        assert_that(response.status_code, is_(200))
        page = BeautifulSoup(response.data)
        assert_that(page.find('h1').text, contains_string('Your Employee Record'))

    @patch("claimants_user_journey.routes.employee_via_nino")
    def test_claimant_is_shown_employee_record_for_nino(self, employee_via_nino):
        employee_via_nino.return_value = {"first_name": "John"}

        test_app = routes.app.test_client()
        response = test_app.get('/claim-redundancy-payment/employee-records/?nino=AB111111C')
        assert_that(response.status_code, is_(200))
        page = BeautifulSoup(response.data)
        assert_that(page.find('h1').text, contains_string('Your Employee Record'))
        assert_that(page.find('pre').text, contains_string('John'))

    @patch("claimants_user_journey.routes.employee_via_nino")
    def test_nino_is_not_case_sensitive(self, employee_via_nino):
        employee_via_nino.return_value = {"first_name": "John"}

        test_app = routes.app.test_client()
        response = test_app.get('/claim-redundancy-payment/employee-records/?nino=ab111111c')
        assert_that(response.status_code, is_(200))
        page = BeautifulSoup(response.data)
        assert_that(page.find('h1').text, contains_string('Your Employee Record'))
        assert_that(page.find('pre').text, contains_string('John'))

    def test_shows_nino_not_found_page_if_nino_not_provided(self):
        test_app = routes.app.test_client()
        response = test_app.get('/claim-redundancy-payment/employee-records/')
        assert_that(response.status_code, is_(200))
        page = BeautifulSoup(response.data)
        assert_that(page.find('h1').text, contains_string('No Employee Record Found'))
