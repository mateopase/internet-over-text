from bot.adapters import facebook

from .parse import parser
from .reddit import build_reddit_reply


def reply(sender_id: str, message: str):
    command = None
    response = None
    buttons = None

    try:
        args = message.split(" ")
        command = parser.parse_args(args)
    except: 
        response = [parser.format_help()]


    if command:
        if command.site == "reddit":
            response, buttons = build_reddit_reply(command)

    facebook.reply(sender_id, response, buttons)


