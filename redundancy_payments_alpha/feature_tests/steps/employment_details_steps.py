from claimants_user_journey import routes

test_client = routes.app.test_client()

@given('a claimant with the employment details')
def step(context):
    context.form_data = {}

    for row in context.table:
        if row['DETAILS'] == 'start_date':
            context.form_data['start_date'] = row['VALUE'].split('/')
        elif row['DETAILS'] == 'end_date':
            context.form_data['end_date'] = row['VALUE'].split('/')
        else:
            context.form_data[row['DETAILS']] = row['VALUE']

@when('enters the employment details')
def step(context):
    context.response = test_client.post(
        '/claim-redundancy-payment/employment-details/',
        data=context.form_data
    )
