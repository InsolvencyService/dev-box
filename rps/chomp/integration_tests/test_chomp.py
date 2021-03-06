import unittest

from hamcrest import assert_that, is_
from mock import patch
from nose.plugins.attrib import attr

from chomp.routes import app as chomp_app
from claim_service import api as claim_service_api
from birmingham_cabinet.api import add_rp14a_form


@attr('integration')
class TestChomp(unittest.TestCase):

    def test_should_return_204_when_no_claims(self):
        test_client = chomp_app.test_client()

        no_claims_response = test_client.get("/chomp/next")

        assert_that(no_claims_response.status_code, is_(204))

    def test_should_redirect_when_claims(self):
        add_rp14a_form(
            {
            "employee_national_insurance_number": "foobar",
            "employee_date_of_birth": "01/10/2003",
            "employee_title" : "Ms",
            "employee_forenames" : "Boo",
            "employee_surname" : "Boo",
            "employer_name" : "Boo"
           }
        )
        claim_service_api.create_claim_2(
            {"nino": "foobar"}
        )

        test_client = chomp_app.test_client()

        no_claims_response = test_client.get("/chomp/next")

        assert_that(no_claims_response.status_code, is_(303))
