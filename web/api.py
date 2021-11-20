from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse


app = Flask(__name__)


"""
Various webhook endpoints to handle communication methods.
SMS -> Twilio
Messenger -> Facebook
WhatsApp? What else?
"""


@app.route("/sms/reply", methods=["POST"])
def sms():
    body = request.values.get("Body", None)



    response = MessagingResponse().message()
    return str(response)


@app.route("/fb/reply", methods=["POST"])
def facebook_messenger():
    return {"message": "Hello, world!"}