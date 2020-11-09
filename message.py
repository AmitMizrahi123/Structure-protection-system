from twilio.rest import Client


def send_message(phone_list):
    account_sid = '<TWILIO_ACCOUNT_SID>'
    auth_token = '<TWILIO_AUTH_TOKEN>'
    client = Client(account_sid, auth_token)

    for phone in phone_list:
        message = client.messages.create(
            body='There is unknown person in the building',
            from_='<TWILIO_FROM>',
            to=phone
        )

        print(message.sid)

        return False
