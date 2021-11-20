import os
import textwrap
import time

from flask import abort, Blueprint, request
import requests

from web.api.auth import facebook_auth
from web.handlers import handle


messenger = Blueprint("facebook", __name__)

FB_VERIFY_TOKEN = os.environ.get("FB_VERIFY_TOKEN")
FB_PAGE_ACCESS_TOKEN = os.environ.get("FB_PAGE_ACCESS_TOKEN")
FB_SEND_API_URL = "https://graph.facebook.com/v12.0/me/messages"

# TODO Put this somewhere else
def respond(sender_id: str, message: dict):
    response_body = {
        "recipient": {"id": sender_id},
        "message": message
    }
    error = requests.post(FB_SEND_API_URL, json=response_body, params={"access_token": FB_PAGE_ACCESS_TOKEN})
    if error.status_code != 200:
        print(error.json())


# TODO Clean this whole thing up, add wrap and button support globally, and nerf SMS
@messenger.route("/messenger/", methods=["POST"])
@facebook_auth
def messenger_reply():
    message = request.json["entry"][0]["messaging"][0]["message"]
    if "quick_reply" in message:
        text = message["quick_reply"]["payload"]
    else:
        text = message["text"]
    sender_id = request.json["entry"][0]["messaging"][0]["sender"]["id"]

    response = handle(text)
    if len(response.message) > 2000:
        messages = textwrap.wrap(response.message, 2000)
        for m in messages[0:-1]:
            content = {"text": m}
            respond(sender_id, content)
            time.sleep(0.2)
        content = {"text": messages[-1], "quick_replies": response.buttons}
        respond(sender_id, content)
    else:
        content = {"text": response.message, "quick_replies": response.buttons}
        respond(sender_id, content)

    return {}


@messenger.route("/messenger/", methods=["GET"])
def verify_webhook():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == FB_VERIFY_TOKEN:
        return challenge
    else:
        abort(403)
