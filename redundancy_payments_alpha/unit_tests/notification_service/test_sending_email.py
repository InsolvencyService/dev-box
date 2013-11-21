import unittest
from mock import patch
from hamcrest import assert_that, is_

from notification_service import api as notifications_api


class TestSendingEmail(unittest.TestCase):
    @patch('notification_service.api.send_email_via_mandrill')
    def test_sending_an_email(self, mock_send_email_via_mandrill):
        to_email = 'foo@bar.com'
        subject = 'an email'
        to_name = 'Mr Foo'
        message_text = 'Some message text'
        from_email = 'to-be-confirmed@rps.com'
        from_name = 'Redundancy Payments Service'

        notifications_api.send_email(
            to_email,
            subject,
            to_name,
            message_text
        )

        mock_send_email_via_mandrill.assert_called_with(
            to_email=to_email,
            to_name=to_name,
            from_email=from_email,
            from_name=from_name,
            subject=subject,
            text=message_text
        )
