import unittest
from BeautifulSoup import BeautifulSoup
from mock import patch

def get_mock_storage():
    return object()

class FormTest(unittest.TestCase):
    def _parse_csrf_token(self, response):
        page = BeautifulSoup(response.data)
        csrf_token = page.find(id='csrf_token')
        if not csrf_token:
            raise Exception("Couldn't find a csrf_token... is the form wired up correctly?")
        return csrf_token['value']

    def submit_form(self, test_client, url, data):
        response = test_client.get(url)
        print response
        data.update({'csrf_token': self._parse_csrf_token(response)})
        return test_client.post(url, data=data)

    def create_form(self, app, url, form_class, **kwargs):
        with app.test_request_context(url):
            form = form_class(**kwargs)
        return form

