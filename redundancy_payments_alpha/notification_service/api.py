import os
from email import _send_email_via_mandrill


def send_email(to_email, subject, to_name, message_text):

    from_email = 'to-be-confirmed@rps.com'
    from_name = 'Redundancy Payments Service'

    use_mock_email = os.environ.get('USE_MOCK_EMAIL', None)

    if(use_mock_email):
        with open('TestEmail.txt', 'w') as f:
            f.write('From Email: %s' % from_email)
            f.write('From Name: %s' % from_name)
            f.write('To Address: %s' % to_email)
            f.write('Subject: %s' % subject)
            f.write('To Name: %s' % to_name)
            f.write('Message Text: %s' % message_text)
    else:
        _send_email_via_mandrill(
            to_email=to_email,
            to_name=to_name,
            from_email=from_email,
            from_name=from_name,
            subject=subject,
            text=message_text
        )

