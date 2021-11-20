from web.handlers import handle

from flask import Flask, request, Response
from twilio.twiml.messaging_response import MessagingResponse


app = Flask(__name__)


"""
Various webhook endpoints to handle communication methods.
SMS -> Twilio
Messenger -> Facebook
WhatsApp? What else?
Can we navigate via SMS in situations w/ poor signal?
"""


@app.route("/sms/reply/", methods=["POST"])
def sms():
    body = request.values.get("Body", None)
    content = handle(body)
    response = MessagingResponse().message(content)

    return Response(str(response), mimetype='text/xml')


@app.route("/fb/reply/", methods=["POST"])
def facebook_messenger():
    return {"message": "Hello, world!"}