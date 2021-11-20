from web.providers import reddit, twitter

from .manual import MANUAL


def handle(message: str) -> str:
    parts = message.lower().split(" ")

    if len(parts) >= 2:
        command, arguments = parts[0], parts[1:]

        if command.startswith("r"):
            return handle_reddit(arguments)
        elif command.startswith("t"):
            return handle_twitter(arguments)
        elif command == "isodd":
            return handle_is_odd(arguments)

    return MANUAL


def handle_reddit(arguments: list) -> str:
    if len(arguments) == 1:
        return reddit.get_subreddit_posts(arguments[0])
    else:
        return reddit.get_post(arguments[0], arguments[1])


def handle_twitter(arguments: list) -> str:
    return twitter.get_user_posts(arguments[0])


def handle_is_odd(arguments: list) -> str:
    num = int(arguments[0])
    result = "is" if str(num % 2 == 1) else "is not"
    return f"{num} {result} odd. The power of modern technology."
