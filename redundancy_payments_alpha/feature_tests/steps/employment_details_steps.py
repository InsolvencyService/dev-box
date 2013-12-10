from claimants_user_journey import routes

test_client = routes.app.test_client()

@given('a claimant with the employment details')
def step(context):
    context.form_data = {}

    start_date = ['','','']
    end_date = ['','','']

    for row in context.table:
        if row['DETAILS'] == 'start_date-day':
            start_date[0] = row['VALUE']
        elif row['DETAILS'] == 'start_date-month':
            start_date[1] = row['VALUE']
        elif row['DETAILS'] == 'start_date-year':
            start_date[2] = row['VALUE']
        elif row['DETAILS'] == 'end_date-day':
            end_date[0] = row['VALUE']
        elif row['DETAILS'] == 'end_date-month':
            end_date[1] = row['VALUE']
        elif row['DETAILS'] == 'end_date-year':
            end_date[2] = row['VALUE']
        else:
            context.form_data[row['DETAILS']] = row['VALUE']

    context.form_data['start_date'] = start_date
    context.form_data['end_date'] = end_date

@when('enters the employment details')
def step(context):
    context.response = test_client.post(
        '/claim-redundancy-payment/employment-details/',
        data=context.form_data
    )
