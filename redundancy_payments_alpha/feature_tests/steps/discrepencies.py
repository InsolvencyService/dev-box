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
        )
    )
    assert_that(response.status_code, is_(302))

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
    print response.data
    assert_that(response.status_code, is_(302))

