import textwrap
import time

import requests

from bot.utils.settings import FB_PAGE_ACCESS_TOKEN

MAX_MESSAGE_LEN = 2000
MESSAGE_DELAY = 0


class Facebook:
    FB_SEND_API_URL = "https://graph.facebook.com/v12.0/me/messages"

    def __init__(self):
        requests.Session
        self.session = requests.Session()

        self.session.params = {"access_token": FB_PAGE_ACCESS_TOKEN}

    def reply(self, sender_id: str, body: str, buttons: list[dict]):
        messages = textwrap.wrap(body, MAX_MESSAGE_LEN)

        for message in messages[0:-1]:
            content = {"text": message}
            self._send_reply(sender_id, content)
            time.sleep(MESSAGE_DELAY)

        content = {
            "text": messages[-1],
            "quick_replies": buttons
        }
        self._send_reply(sender_id, content)


    def _send_reply(self, sender_id: str, message: dict):
        response_body = {
            "recipient": {"id": sender_id},
            "message": message
        }

        # Minimal effort, just try sending once
        self.session.post(self.FB_SEND_API_URL, json=response_body)
