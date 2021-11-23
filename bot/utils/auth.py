import hmac
import hashlib
from functools import wraps

from flask import abort, request

from bot.utils.settings import FB_APP_SECRET


def facebook_auth(route):
    """
    Simple auth wrapper for validating Facebook API key.
    """

    @wraps(route)
    def decorated_route(*args, **kwargs):
        # Get sig from request
        request_sig = request.headers.get(
            key="X-Hub-Signature", default="").removeprefix("sha1=")

        # Calculate signature request should have
        expected_sig = hmac.new(
            bytes(FB_APP_SECRET, "utf-8"),
            request.get_data(),
            hashlib.sha1
        ).hexdigest()

        # Check that request signature matches expected
        if not hmac.compare_digest(expected_sig, request_sig):
            abort(401)

        return route(*args, **kwargs)

    return decorated_route
