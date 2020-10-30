from flask import Flask, request
from flask_ngrok import run_with_ngrok
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)
run_with_ngrok(app)


@app.route('/sms', methods=['GET', 'POST'])
def sms():
    body = request.values.get('body', None)
    resp = MessagingResponse()

    '''
        Do something....
    '''

    return str(resp)


if __name__ == '__main__':
    app.run()