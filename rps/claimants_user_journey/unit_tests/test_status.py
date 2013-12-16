from claimants_user_journey import routes
import unittest

test_client = routes.app.test_client()

class TestStatus(unittest.TestCase):
    def test_status(self):
        response = test_client.get('/_status')
        self.assertEqual(response.data, 'everything is ok')

