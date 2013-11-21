from behave import *
from mock import patch
from insolvency_practitioner_forms.routes import app as a

from birmingham_cabinet.api import add_rp14a_form
from claim_service.api import submit, create_claim_2
import notification_service.email

@given(u'the claimant has submitted a claim')
def impl(context):
    rp14a = {
        "employee_national_insurance_number": "AB111111C",
        "employee_date_of_birth": "01/01/1900",
        "employee_title": "Mr",
        "employee_forenames": "John",
        "employee_surname": "Smith",
        "ip_number": "0000",
        "employer_name": "Widgets Co",
        "employee_basic_weekly_pay": "550"
    }
    add_rp14a_form(rp14a)
    personal_details = {"nino": "AB111111C"}
    claim_id = create_claim_2(personal_details)
    submit(claim_id)


@when("The notifications are triggered")
def step(context):
    test_client = a.test_client()
    test_client.post('/_tasks/send-notifications/')

@then("the email is sent to the IP")
@patch('notification_service.api.send_email')
def step(context, mock_email_service):
    mock_email_service.assert_called_with('something')
