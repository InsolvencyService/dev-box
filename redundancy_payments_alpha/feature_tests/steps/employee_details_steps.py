from datetime import date

from birmingham_cabinet.api import employee_via_nino, add_rp14a_form
from insolvency_practitioner_forms import routes

ip_test_client = routes.app.test_client()

@given('an employee with the nino {nino}')
def step(context, nino):
    add_rp14a_form({
        "employee_national_insurance_number": nino,
        "employee_date_of_birth": date(2013, 1, 1),
        "employee_title": "Mr",
        "employee_forenames": "Donald",
        "employee_surname": "Duck",
        "employer_name": "Duck Enterprises",
    })

@given('an IP entering the employee details')
def step(context):
    context.form_data = {}
    for row in context.table:
        context.form_data[row['DETAILS']] = row['VALUE']

@when('the IP goes to {url}')
def step(context, url):
    form = ip_test_client.get(url)
    context.form_data['csrf_token'] = parse_csrf_token(form)

@when('enters the employee details')
def step(context):
    context.response_from_posting_data = ip_test_client.post(
        '/create-employee-record/employee-details/',
        data=context.form_data
    )

@then('the IP should be sent to {url}')
def step(context, url):
    assert_that(context.response_from_posting_data.status, is_('302 FOUND'))
    headers = context.response_from_posting_data.headers
    redirect_path = headers['Location']
    assert_that(redirect_path, contains_string(url))


@then("the data base should contain an employee")
def step(context):
    nino = context.form_data["employee_national_insurance_number"]
    employee = employee_via_nino(nino)
    assert_that(employee, is_(not_none()))
