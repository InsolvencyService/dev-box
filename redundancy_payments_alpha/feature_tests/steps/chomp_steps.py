from birmingham_cabinet.api import add_rp14a_form
from chomp.api import evaluate_forms
from chomp.routes import app as chomp_app
from claim_service.api import create_claim_2

from behave import *
from mock import patch
from hamcrest import assert_that, is_
from urlobject import URLObject


@then('the chomp service should generate an xml payload containing {name}')
def step(context, name):
    xml_payload = evaluate_forms()
    assert_that(xml_payload, string_contains_in_order(name))


@given('a claim exists')
def step(context):
    rp14a = {
        "employee_national_insurance_number": "AB123456Z",
        "employee_date_of_birth": "01/01/1900",
        "employee_title": "Mr",
        "employee_forenames": "John",
        "employee_surname": "Smith",
        "ip_number": "0000",
        "employer_name": "Widgets Co",
        "employee_basic_weekly_pay": "550"
    }
    add_rp14a_form(rp14a)
    personal_details = {"nino": "AB123456Z"}
    context.claim_id = create_claim_2(personal_details)

@when("we ask for the next claim")
def step(context):
    context.test_client = chomp_app.test_client()
    context.response_for_next = context.test_client.post("/chomp/next")

@then("we are redirected to the next claim")
def step(context):
    assert_that(context.response_for_next.status_code, is_(303))
    context.claim_location = context.response_for_next.headers["Location"]
    assert_that(context.claim_location,
                matches_regexp("http://localhost/chomp/\d+/"))

@then("that claim's status is In Progress")
def step(context):
    status_url = URLObject(context.claim_location).add_path_segment("status")
    print status_url
    response_for_status = context.test_client.get(status_url)
    assert_that(response_for_status.data, is_("In Progress"))
