from behave import *
from hamcrest import *
import claimants_user_journey.routes

@given('the app is running')
def step(context):
    context.client = claimants_user_journey.routes.app.test_client()

@when('we visit {url}')
def step(context, url):
    context.response = context.client.get(url)

@then('the page should include "{content}"')
def step(context, content):
    assert_that(context.response.data, contains_string(content))

@then('the page should have title "{expected_title}"')
def step(context, expected_title):
    assert_that(context.response.data,
                contains_string('<title>%s</title>' % expected_title))

@then('the page should have subtitle "{expected_subtitle}"')
def step(context, expected_subtitle):
    assert_that(context.response.data,
                contains_string('<h4 class="subtitle">%s</h4>' % expected_subtitle))

@then('the page should have an input field called "{input_name}" labeled "{label_name}"')
def step(context, input_name, label_name):
    #TODO: better testing for HTML elements
    assert_that(context.response.data, contains_string('name="%s"' % input_name))
    assert_that(context.response.data, contains_string('%s</label>' % label_name))
