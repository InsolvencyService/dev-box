from email import send_email_via_mandrill


def send_email(to_email, subject, to_name, message_text):

    from_email = 'to-be-confirmed@rps.com'
    from_name = 'Redundancy Payments Service'

    send_email_via_mandrill(
        to_email=to_email,
        to_name=to_name,
        from_email=from_email,
        from_name=from_name,
        subject=subject,
        text=message_text
    )

