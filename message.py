from twilio.rest import Client


def send_message(phone_list):
    account_sid = '<ACCOUNT SID TWILIO>'
    auth_token = '<AUTH TOKEN TWILIO>'
    client = Client(account_sid, auth_token)

    for phone in phone_list:

        message = client.messages.create(
            body='<BODY MESSAGE>',
            from_='<TWILIO NUMBER>',
            to=phone
        )

        print(message.status)
