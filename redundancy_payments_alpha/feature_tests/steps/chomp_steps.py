from birmingham_cabinet.api import (
    add_rp14a_form,
    get_next_claim_not_processed_by_chomp
)
from chomp.api import evaluate_forms
from chomp.routes import app as chomp_app
from claim_service.api import create_claim_2

from behave import *
from mock import patch
from hamcrest import assert_that, is_, contains_string
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
    state_url = URLObject(context.claim_location).add_path_segment("state")
    response_for_status = context.test_client.get(state_url)
    assert_that(response_for_status.data, is_("In Progress"))

@given('a claim is in In Progress')
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
    get_next_claim_not_processed_by_chomp()

@when('we set the state to {state}')
def step(context, state):
    context.test_client = chomp_app.test_client()
    claim_id = context.claim_id
    response_for_post = context.test_client.post(
        "/chomp/{claim_id}/state".format(**locals()), data=state)
    assert_that(response_for_post.status_code, is_(200))


@then('the state is {state}')
def step(context, state):
    claim_id = context.claim_id
    response_for_get = context.test_client.get(
        "/chomp/{claim_id}/state".format(**locals()))
    assert_that(response_for_get.data, is_(state))


@then('we can get the acceptdoc')
def step(context):
    claim_id = context.claim_id
    response_for_acceptdoc = chomp_app.test_client().get(
        "/chomp/{claim_id}/acceptdoc".format(**locals()))
    assert_that(response_for_acceptdoc.status_code, is_(200))
    assert_that(response_for_acceptdoc.content_type,
                contains_string("text/xml"))
    assert_that(response_for_acceptdoc.data,
                contains_string("CHAMP Acceptdoc Payload"))


@then('we can get the rp1')
def step(context):
    claim_id = context.claim_id
    response_for_rp1 = chomp_app.test_client().get(
        "/chomp/{claim_id}/rp1".format(**locals()))
    assert_that(response_for_rp1.status_code, is_(200))
    assert_that(response_for_rp1.content_type,
                contains_string("text/xml"))
    assert_that(response_for_rp1.data,
                contains_string("CHAMP RP1 Payload"))


@then('we can get the rp14')
def step(context):
    claim_id = context.claim_id
    response_for_rp14 = chomp_app.test_client().get(
        "/chomp/{claim_id}/rp14".format(**locals()))
    assert_that(response_for_rp14.status_code, is_(200))
    assert_that(response_for_rp14.content_type,
                contains_string("text/xml"))
    assert_that(response_for_rp14.data,
                contains_string("CHAMP RP14 Payload"))


@then('we can get the rp14a')
def step(context):
    claim_id = context.claim_id
    response_for_rp14a = chomp_app.test_client().get(
        "/chomp/{claim_id}/rp14a".format(**locals()))
    assert_that(response_for_rp14a.status_code, is_(200))
    assert_that(response_for_rp14a.content_type,
                contains_string("text/xml"))
    assert_that(response_for_rp14a.data,
                contains_string("CHAMP RP14A Payload"))
