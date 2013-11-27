from hamcrest import assert_that, contains_string
from birmingham_cabinet import api as cabinet_api

@then('the page should have text "{text}"')
def step(context, text):
    assert_that(context.response.data, contains_string(text))

@given('there are claims in the database')
def step(context):
    #No discrepancies
    claimant_data_1 = {'nino': 'XX223344X', 'gross_rate_of_pay': 100}
    employee_record_1 = {'employer_id': 1, 'employee_basic_weekly_pay': 100}

    cabinet_api.add_claim(claimant_data_1, employee_record_1)

    #With discrepancies
    claimant_data_2 = {'nino': 'XX223355A', 'gross_rate_of_pay': 100}
    employee_record_2 = {'employer_id': 1, 'employee_basic_weekly_pay': 200}

    cabinet_api.add_claim(claimant_data_2, employee_record_2)#
