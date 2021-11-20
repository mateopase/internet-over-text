import os

from flask import abort, Blueprint, request
import requests

from web.api.auth import facebook_auth


messenger = Blueprint("facebook", __name__)

FB_VERIFY_TOKEN = os.environ.get("FB_VERIFY_TOKEN")
FB_PAGE_ACCESS_TOKEN = os.environ.get("FB_PAGE_ACCESS_TOKEN")
FB_SEND_API_URL = "https://graph.facebook.com/v12.0/me/messages"


def respond(sender_id: str, message: dict):
    response_body = {
        "recipient": {"id": sender_id},
        "message": message
    }
    requests.post(FB_SEND_API_URL, json=response_body, params={"access_token": FB_PAGE_ACCESS_TOKEN})


@messenger.route("/messenger/", methods=["POST"])
@facebook_auth
def messenger_reply():
    response = {"text": "hey there"}
    sender_id = request.json["entry"][0]["messaging"][0]["sender"]["id"]

    # respond(sender_id, response)
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
