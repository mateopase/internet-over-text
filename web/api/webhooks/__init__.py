"""
Various webhook endpoints to handle communication methods.
Messenger -> Facebook
SMS -> Twilio
WhatsApp? What else?
Can we navigate via SMS in situations w/ poor signal?
"""

from .messenger import messenger
from .sms import sms