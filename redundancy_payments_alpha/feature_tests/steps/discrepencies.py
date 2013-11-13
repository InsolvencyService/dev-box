from behave import *
from birmingham_cabinet import api
from claimants_user_journey.routes import app
from hamcrest import *
from BeautifulSoup import BeautifulSoup

@given('the IP has provided the employee details')
def step(context):
    employee_details = {}
    for key, value in context.table:
        employee_details[key] = value
    api.add_rp14a_form(employee_details)
    context.nino = employee_details['nino']

def parse_csrf_token(response):
    # in order to post form data back to the app
    # we need to also send back the csrf token
    page = BeautifulSoup(response.data)
    csrf_token = page.find('input', id='csrf_token')['value']
    return csrf_token

@given('the claimant is matched to the employee details')
def step(context):
    context.app = app.test_client()
    get_the_page = context.app.get('/claim-redundancy-payment/personal-details/')
    response = context.app.post(
        '/claim-redundancy-payment/personal-details/',
        data = dict(
            forenames='John',
            surname='Smith',
            title='Mr',
            other='',
            building_number='0',
            street='Fake Street',
            district='9',
            town_or_city='Fake Town',
            county='Not-a-county',
            postcode='XXXXXX',
            email='foo@bar.com',
            telephone_number='000000 000 000',
            nino=context.nino,
            date_of_birth='01/01/1900',
            csrf_token=parse_csrf_token(get_the_page)
        ),
        follow_redirects=True
    )
    assert_that(response.status_code, is_(200))
    page = BeautifulSoup(response.data)
    assert_that(page.find('h1').text, is_('Your Employee Record'))

@when('the claimant enters the valid wage details')
def step(context):
    wages_details = {}
    for key, value in context.table:
        wages_details[key] = value
    get_the_page = context.app.get('/claim-redundancy-payment/wage-details/')
    wages_details.update({'csrf_token': parse_csrf_token(get_the_page)})
    response = context.app.post(
        '/claim-redundancy-payment/wage-details/',
        data=wages_details
    )
    assert_that(response.status_code, is_(302))
    assert_that(response.headers, has_entry(
        'Location',
        contains_string('/claim-redundancy-payment/wage-details/discrepancies')
    ))
    followup_response = context.app.get(
       '/claim-redundancy-payment/wage-details/discrepancies/' 
       )
    assert_that(followup_response.status_code, is_(200))
    context.followup_response = followup_response


@then('the claimant should see a discrepancy on gross rate of pay')
def step(context):
    discrepancy_html = context.followup_response.data
    page = BeautifulSoup(discrepancy_html)
    question_element = page.find(id="gross_rate_of_pay_question")
    assert_that(question_element['class'], contains_string('discrepancy'))


@then('not see a discrepancy on normal days of work')
def step(context):
    discrepancy_html = context.followup_response.data
    page = BeautifulSoup(discrepancy_html)
    question_element = page.find(id="gross_rate_of_pay_question")
    assert_that(question_element['class'], is_not(contains_string('discrepancy')))

