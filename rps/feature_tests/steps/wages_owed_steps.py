from claimants_user_journey import routes


@given('a claimant with the unpaid wage details')
def step(context):
    context.form_data = {}
    for row in context.table:
        context.form_data[row['DETAILS']] = row['VALUE']

@when('enters the unpaid wages details')
def step(context):
    context.response_from_posting_data = test_client.post(
        '/claim-redundancy-payment/wages-owed-details/',
        data=context.form_data
    )
