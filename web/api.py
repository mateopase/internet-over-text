from web.auth import twilio_auth
from web.handlers import handle

from flask import Flask, request, Response
from twilio.twiml.messaging_response import MessagingResponse, Message


app = Flask(__name__)


"""
Various webhook endpoints to handle communication methods.
SMS -> Twilio
Messenger -> Facebook
WhatsApp? What else?
Can we navigate via SMS in situations w/ poor signal?
"""


@app.route("/sms/reply/", methods=["POST"])
@twilio_auth
def sms():
    body = request.values.get("Body", None)
    content = handle(body)

    response = MessagingResponse()
    message = Message()
    message.body(content)
    response.append(message)

    return Response(str(response), mimetype='text/xml')


# @app.route("/fb/reply/", methods=["POST"])
def messenger():
    return {"message": "Hello, world!"}