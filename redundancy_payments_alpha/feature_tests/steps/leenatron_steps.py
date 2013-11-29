import os
from behave import *
from mock import patch
from hamcrest import assert_that, is_
from insolvency_practitioner_forms.routes import app as a

from birmingham_cabinet.api import add_rp14a_form
from claim_service.api import submit, create_claim_2
import notification_service


@given(u'the claimant has created a claim')
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


@when("the claimant submits the claim")
def step(context):
    submit(context.claim_id)


@then("the queue should have the claim on it")
def step(context):
    raise NotImplementedError()
