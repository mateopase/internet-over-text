from flask import Blueprint


static = Blueprint("static", __name__)


@static.route("/auth/callback/", methods=["GET"])
def reddit_auth_callback():
    return "Not used."


@static.route("/privacy/", methods=["GET"])
def fb_privacy():
    return "We don't store or log anything :)"


@static.route("/tos/", methods=["GET"])
def fb_tos():
    return "Not used yet."