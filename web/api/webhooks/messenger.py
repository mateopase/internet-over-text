import os

from flask import abort, Blueprint, request
import requests

from web.api.auth import facebook_auth


messenger = Blueprint("facebook", __name__)
FB_VERIFY_TOKEN = os.environ.get("FB_VERIFY_TOKEN")


def respond(message: dict):
    pass


@messenger.route("/messenger/", methods=["POST"])
@facebook_auth
def messenger_reply():
    respond(request.json)
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
