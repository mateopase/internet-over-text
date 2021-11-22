from argparse import Namespace

from bot.providers import reddit


def build_reddit_reply(command: Namespace) -> tuple[str, list[dict]]:
    if command.content == "subreddit":
        return build_subreddit_reply(command.subreddit, command.page, command.sort, command.time)
    elif command.content == "post":
        return build_post_reply(command.post_id)
    elif command.content == "comments":
        return build_comment_reply(command.post_id, command.page, command.sort)


"""
[
{
    "content_type": "text",
    "title": post,
    "payload": f"r {arguments[0]} {post}",
},
{...}
]
Buttons: previous page, next page, top
"""
def build_subreddit_reply(sub: str, page: int, sort: str, time: str) -> tuple[str, list[dict]]:
    posts = reddit.list_posts(sub, page, sort, time)
    display_names = [
        f"{post.title} | {post.subreddit.display_name}\nV: {post.score}, C: {post.num_comments}"
        for post in posts.items
    ]
    response = "\n\n".join(display_names)
    return response or f"No more posts on /r/{sub}", None


def build_post_reply(post_id: str) -> tuple[str, list[dict]]:
    post = reddit.get_post(post_id)
    return post.selftext or "No post body or this is an image post :'(", None


def build_comment_reply(post_id: str, page: int, sort: str) -> tuple[str, list[dict]]:
    comments = reddit.get_post_comments(post_id, page, sort)
    response = "\n\n".join([comment.body for comment in comments.items])
    return response or "No more comments :'(", None
