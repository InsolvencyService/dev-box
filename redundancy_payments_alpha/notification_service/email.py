import mandrill
from config import API_KEY

def _send_email_via_mandrill(to_email, to_name, from_email, from_name, subject, text):

    mandrill_api = mandrill.Mandrill(API_KEY)
    message = {
        'auto_text': True,
        'from_email': from_email,
        'from_name': from_name,
        'headers': { 'Reply-To': from_email },
        'important': False,
        'subject': subject,
        'text': text,
        'to': [{'email': to_email, 'name': to_name, 'type': 'to'}]
    }

    mandrill_api.messages.send(
        message=message,
        async=False,
        ip_pool='Main Pool'
    )

