from dataclasses import dataclass

from web.providers import reddit, twitter, wikipedia

from .manual import MANUAL


@dataclass
class HandlerResponse:
    message: str
    buttons: object


def handle(message: str) -> HandlerResponse:
    parts = message.lower().split(" ")

    if len(parts) >= 2:
        command, arguments = parts[0], parts[1:]

        if command.startswith("r"):
            return handle_reddit(arguments)
        elif command.startswith("t"):
            return handle_twitter(arguments)
        elif command.startswith("w"):
            return handle_wikipedia(arguments)
        elif command == "isodd":
            return handle_is_odd(arguments)

    return HandlerResponse(MANUAL)


def handle_reddit(arguments: list) -> str:
    if len(arguments) == 1:
        posts = reddit.get_subreddit(arguments[0])
        titles = [f"[{num}] {post.title} | {post.subreddit.display_name}" for num, post in enumerate(posts, start=1)]
        buttons = [
            {
                "content_type": "text",
                "title": post,
                "payload": f"r {arguments[0]} {post}",
            }
            for post in range(1, len(titles) + 1)
        ]

        return HandlerResponse("\n".join(titles), buttons)
    else:
        return HandlerResponse(reddit.get_post(arguments[0], int(arguments[1])))


def handle_twitter(arguments: list) -> str:
    return HandlerResponse(twitter.get_user_posts(arguments[0]))


def handle_wikipedia(arguments: list) -> str:
    return HandlerResponse(wikipedia.get_article(arguments[0]))


def handle_is_odd(arguments: list) -> str:
    num = int(arguments[0])
    result = "is" if num % 2 == 1 else "is not"
    return HandlerResponse(f"{num} {result} odd. The power of modern technology.")
