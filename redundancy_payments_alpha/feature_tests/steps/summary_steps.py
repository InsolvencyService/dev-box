from claimants_user_journey import routes

@when('the claimant views the summary page')
def step(context):
    form = context.app.get('/claim-redundancy-payment/summary/')
    context.response=form