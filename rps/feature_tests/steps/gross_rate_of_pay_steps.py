from behave import *
from BeautifulSoup import BeautifulSoup
from hamcrest import assert_that, is_

from claimants_user_journey.routes import app


def _get_csrf_token_from_page(url, app):
    response = app.get(url)
    soup = BeautifulSoup(response.data)
    token = soup.find(id='csrf_token')['value']
    return token


@given('a claimant who gets paid {amount} pounds a {period} fills out the calculator')
def step(context, amount, period):
    context.app = app.test_client()
    context.response = context.app.post(
        '/claim-redundancy-payment/wage-amount/',
        data={
            'period': period,
            'gross_pay': amount,
            'csrf_token': _get_csrf_token_from_page(
                '/claim-redundancy-payment/wage-amount/',
                context.app
                )
        },
        follow_redirects=True
    )


@when('their gross rate of pay is calculated')
def step(context):
   soup = BeautifulSoup(context.response.data)
   context.calculator_result = soup.find('strong').text[1:] #strip off pound sign


@then('the weekly gross rate of pay returned should be {result} pounds')
def step(context, result):
    assert_that(context.calculator_result, is_(result))


@then('the wage details page should have gross rate of pay prepopulated')
def step(context):
    response = context.app.get('/claim-redundancy-payment/wage-details/')
    soup = BeautifulSoup(response.data)
    prepopulated_value = soup.find(id='gross_rate_of_pay')['value']
    assert_that(prepopulated_value, is_(context.calculator_result))

