from datetime import date
from hamcrest import assert_that, contains_string
from birmingham_cabinet import api as cabinet_api

@then('the page should have text "{text}"')
def step(context, text):
    assert_that(context.response.data, contains_string(text))

@then('the page should have text that is the current date')
def step(context):
    assert_that(context.response.data,
                contains_string(date.today().strftime('%d/%m/%Y')))

@given('there are claims in the database')
def step(context):
    #No discrepancies
    claimant_data_1 = {'nino': 'XX223344X',
                       'forenames': 'Ted Rocket Man',
                       'surname': 'Jones',
                       'date_of_birth': ['23','05','1982'],
                       'gross_rate_of_pay': 100}
    employee_record_1 = {'employer_id': 1,
                         'employee_forenames': 'Ted Rocket Man',
                         'employee_surname': 'Jones',
                         'employee_national_insurance_number': 'XX223344X',
                         'employee_basic_weekly_pay': 100}

    claim_id = cabinet_api.add_claim(claimant_data_1, employee_record_1)
    cabinet_api.mark_claim_as_submitted(claim_id)

    #With discrepancies
    claimant_data_2 = {'nino': 'XX223355A',
                       'forenames': 'John',
                       'surname': 'Henry',
                       'date_of_birth': ['24', '05', '1981'],
                       'gross_rate_of_pay': 200}
    employee_record_2 = {'employer_id': 1,
                         'employee_forenames': 'John',
                         'employee_surname': 'Henry',
                         'nino': 'XX223355A',
                         'employee_basic_weekly_pay': 250}

    claim_id = cabinet_api.add_claim(claimant_data_2, employee_record_2)
    cabinet_api.mark_claim_as_submitted(claim_id)

