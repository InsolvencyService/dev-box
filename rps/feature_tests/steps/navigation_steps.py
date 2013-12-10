from behave import *
from hamcrest import *
from ..claimants_user_journey import routes
from BeautifulSoup import BeautifulSoup

client = routes.app.test_client()


@given('the form pages')
def step(context):
    context.urls = []
    for row in context.table:
        context.urls.append(row['PAGE'])


@when('visiting each form page')
def step(context):
    context.pages = []
    for url in context.urls:
        response = client.get(url)
        page = BeautifulSoup(response.data)
        context.pages.append(page)


@then('we should see a navigation bar with these links')
def step(context):
    for page in context.pages:
        nav_bar = page.find('nav')
        for row in context.table:
            assert_that(str(nav_bar), contains_string(row['LINK']))

