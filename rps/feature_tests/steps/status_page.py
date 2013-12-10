from behave import *
from hamcrest import *
from hamcrest.core.base_matcher import BaseMatcher
from BeautifulSoup import BeautifulSoup

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

@then('the page should have section titled "{expected_section_title}"')
def step(context, expected_section_title):
    assert_that(context.response.data,
                contains_string('<legend>%s</legend>' % expected_section_title))

@then('the page should have an input field called "{name}" labeled "{label}"')
def step(context, name, label):

    def is_dictlike_with_item(name, value):
        """Custom matcher for inputs because pyhamcrests' has_entry matcher
        insists on dict"""
        class IsDictlikeWithItem(BaseMatcher):
            def __init__(self, name, value):
                self.name = name
                self.value = value

            def _matches(self, item):
                # FIXME: Should be ==
                name_ = item.get(self.name, None)
                if name_ is None:
                    return False
                else:
                    return name_.startswith(self.value)

            def describe_to(self, description):
                description.append_text("dictlike with ({name}, {value})".format(
                    name=repr(self.name), value=repr(self.value)))
        return IsDictlikeWithItem(name, value)

    soup = BeautifulSoup(context.response.data)
    inputs = soup.findAll(["input", "select", "textarea"])
    assert_that(inputs, has_item(is_dictlike_with_item("name", name)))

    labels = soup.findAll(["label"])
    assert_that(labels, has_item(has_property("string", label)))
