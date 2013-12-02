@when('the claimant views the summary page')
def step(context):
    form = test_client.get('/claim-redundancy-payment/summary/')
    context.response=form