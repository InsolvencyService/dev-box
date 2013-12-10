from claimants_user_journey import routes

test_client = routes.app.test_client()

@given('a claimant with the holiday pay details')
def step(context):
    context.form_data = {}
    for row in context.table:
        context.form_data[row['DETAILS']] = row['VALUE']

@when('enters the holiday pay details')
def step(context):
    context.response = test_client.post(
        '/claim-redundancy-payment/holiday-pay/',
        data=context.form_data
    )

