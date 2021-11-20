from web.api.auth import facebook_auth, twilio_auth
from web.handlers import handle

from flask import Blueprint, request, Response
from twilio.twiml.messaging_response import MessagingResponse, Message


sms = Blueprint("sms", __name__)


@sms.route("/sms/", methods=["POST"])
@twilio_auth
def sms_reply():
    body = request.values.get("Body", None)
    content = handle(body)

    response = MessagingResponse()
    message = Message()
    message.body(content)
    response.append(message)

    return Response(str(response), mimetype='text/xml')
