from hamcrest import assert_that, is_
from claimants_user_journey import routes
from BeautifulSoup import BeautifulSoup


def parse_csrf_token(response):
    # in order to post form data back to the app
    # we need to also send back the csrf token
    page = BeautifulSoup(response.data)
    csrf_token = page.find('input', id='csrf_token')['value']
    return csrf_token


@when('the claimant views the summary page')
def step(context):
    form = context.app.get('/claim-redundancy-payment/summary/')
    context.response=form


@when('the claimant enters the valid wages owed details')
def step(context):
    wages_owed = {}
    for key, value in context.table:
        wages_owed[key] = value
    get_the_page = context.app.get('/claim-redundancy-payment/wages-owed-details/')
    wages_owed.update({'csrf_token': parse_csrf_token(get_the_page)})
    response = context.app.post(
        '/claim-redundancy-payment/wages-owed-details/',
        data=wages_owed,
        follow_redirects=True
    )
    assert_that(response.status_code, is_(200))
    context.followup_response = response
