from web.providers import npr, reddit, twitter

from .manual import MANUAL


def handle(message: str) -> str:
    parts = message.lower().split(" ")

    if len(parts) > 1:
        command, arguments = parts[0], parts[1:]
    elif len(parts) == 1:
        command, arguments = parts[0], None
    else:
        command = None

    if not command or command == "man":
        return MANUAL
    elif command.startswith("r"):
        return handle_reddit(arguments)
    elif command.startswith("t"):
        return handle_twitter(arguments)
    elif command.startswith("n"):
        return handle_npr(arguments)


def handle_reddit(arguments: list):
    if len(arguments) == 0:
        return reddit.get_subreddit_posts("all")
    elif len(arguments) == 1:
        return reddit.get_subreddit_posts(arguments[0])
    else:
        return reddit.get_subreddit_posts(arguments[0], arguments[1])


def handle_twitter(): ...


def handle_npr(): ...
