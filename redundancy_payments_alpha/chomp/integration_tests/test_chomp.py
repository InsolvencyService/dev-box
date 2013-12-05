import json
import unittest

from hamcrest import assert_that, is_
from mock import patch
from nose.plugins.attrib import attr

from chomp.routes import app as chomp_app
from claim_service import api as claim_service_api
from birmingham_cabinet.api import add_rp14a_form, truncate_all_tables


@attr('integration')
class TestChomp(unittest.TestCase):

    def setUp(self):
        truncate_all_tables()

    def prepare_claim(self):
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
        return claim_service_api.create_claim_2(
            {"nino": "foobar"}
        )

    def test_should_redirect_when_claims_available(self):
        self.prepare_claim()
        test_client = chomp_app.test_client()
        next_response = test_client.get("/chomp/next")
        assert_that(next_response.status_code, is_(303))

        state_url = next_response.headers["Location"] + "state"
        state_response = test_client.get(state_url)
        assert_that(state_response.status_code, is_(200))
        assert_that(state_response.data, is_("In Progress"))

    def test_should_return_204_when_no_claims(self):
        test_client = chomp_app.test_client()
        next_response = test_client.get("/chomp/next")
        assert_that(next_response.status_code, is_(204))

    def test_should_be_able_to_set_state_to_done(self):
        self.prepare_claim()
        test_client = chomp_app.test_client()
        next_response = test_client.get("/chomp/next")
        state_url = next_response.headers["Location"] + "state"
        test_client.post(state_url, data="Done")
        state_response = test_client.get(state_url)

        assert_that(state_response.status_code, is_(200))
        assert_that(state_response.data, is_("Done"))

    def test_should_be_able_to_get_chomp_claim_by_id(self):
        claim_id = self.prepare_claim()
        test_client = chomp_app.test_client()
        response = test_client.get("/chomp/1/")

        assert_that(response.status_code, is_(200))
        response_data = json.loads(response.data)
        assert_that(
            response_data,
            is_({
                "claim": {
                    "claim_id": 1,
                    "state": "Ready"
                }
            }))


    def test_should_be_able_to_return_404_if_no_claim(self):
        test_client = chomp_app.test_client()
        response = test_client.get("/chomp/1/")

        assert_that(response.status_code, is_(404))
