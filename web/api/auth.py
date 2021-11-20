import os
from functools import wraps

from flask import abort, request
from twilio.request_validator import RequestValidator


validator = RequestValidator(os.environ.get('TWILIO_AUTH_TOKEN'))

def twilio_auth(route):
    """
    Simple auth wrapper for validating Twilio API key.
    """

    @wraps(route)
    def decorated_route(*args, **kwargs):
        twilio_sig = request.headers.get(key="X-Twilio-Signature", default="")

        if not validator.validate(request.url, request.form, twilio_sig):
            abort(401)

        return route(*args, **kwargs)

    return decorated_route


def facebook_auth(route):
    """
    Simple auth wrapper for validating Facebook API key.
    """

    @wraps(route)
    def decorated_route(*args, **kwargs):
        hub_signature = request.headers.get(key="X-Hub-Signature", default="")

        if not hub_signature:
            abort(401)

        return route(*args, **kwargs)

    return decorated_route