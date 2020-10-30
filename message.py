from twilio.rest import Client
import os
from dotenv import load_dotenv

load_dotenv()


def send_message(phone_list):
    account_sid = os.getenv('ACCOUNT_SID')
    auth_token = os.getenv('AUTH_TOKEN')
    client = Client(account_sid, auth_token)

    for phone in phone_list:

        message = client.messages.create(
            body=os.getenv('BODY_MSG_TWILIO'),
            from_=os.getenv('FROM_TWILIO'),
            to=phone
        )

        print(message.status)
