from hamcrest import *
from BeautifulSoup import BeautifulSoup
from insolvency_practitioner_forms import routes

ip_routes_app = routes.app

@given('the IP app is running')
def step(context):
    context.client = ip_routes_app.test_client()
