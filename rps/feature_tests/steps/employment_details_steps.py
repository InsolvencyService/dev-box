from claimants_user_journey import routes

test_client = routes.app.test_client()

@given('a claimant with the employment details')
def step(context):
    context.form_data = {}
    for row in context.table:
        context.form_data[row['DETAILS']] = row['VALUE']


@when('enters the employment details')
def step(context):
    context.response_from_posting_data = test_client.post(
        '/claim-redundancy-payment/employment-details/',
        data=context.form_data
    )
