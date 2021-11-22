def get_message(req: dict):
    message = req["entry"][0]["messaging"][0]["message"]

    # Prioritize quick reply payload
    if "quick_reply" in message:
        return message["quick_reply"]["payload"]
    else:
        return message["text"]


def get_sender(req: dict):
    return req["entry"][0]["messaging"][0]["sender"]["id"]