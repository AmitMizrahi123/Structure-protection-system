from twilio.rest import Client


def send_message(phone_list):
    account_sid = 'ACd90b1227023215c5a7c28c27c48a310f'
    auth_token = 'f09c8d8a1af9514cbf6c4626b9049501'
    client = Client(account_sid, auth_token)

    for phone in phone_list:

        message = client.messages.create(
            body='יש מישהו לא מוכר בחווה',
            from_='+12053748923',
            to=phone
        )

        print(message.status)
