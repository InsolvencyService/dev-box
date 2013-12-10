from unit_tests.test_status import test_client


@given('a claimant with the unpaid wage details')
def step(context):
    context.form_data = {}

    for row in context.table:
        if row['DETAILS'] == 'wage_owed_from':
            context.form_data['wage_owed_from'] = row['VALUE'].split('/')
        elif row['DETAILS'] == 'wage_owed_to':
            context.form_data['wage_owed_to'] = row['VALUE'].split('/')
        else:
            context.form_data[row['DETAILS']] = row['VALUE']


@when('enters the unpaid wages details')
def step(context):
    context.response = test_client.post(
        '/claim-redundancy-payment/wages-owed-details/',
        data=context.form_data
    )
