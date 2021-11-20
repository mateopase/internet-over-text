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
        if not validator.validate(request.url, request.form, request.headers.get('X-Twilio-Signature')):
            abort(401)

        return route(*args, **kwargs)

    return decorated_route
