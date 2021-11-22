from flask import abort, Blueprint, request

from bot.core import reply
from bot.utils.auth import facebook_auth
from bot.utils.settings import FB_VERIFY_TOKEN
from bot.utils.request_helper import (
    get_message,
    get_sender,
)


messenger = Blueprint("facebook", __name__)


@messenger.route("/messenger/", methods=["POST"])
@facebook_auth
def messenger_reply():
    sender_id = get_sender(request.json)
    message = get_message(request.json)

    reply(sender_id, message)
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
