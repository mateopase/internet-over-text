from argparse import Namespace

from bot.providers import reddit


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
def build_reddit_reply(command: Namespace) -> tuple[str, list[dict]]:
    if command.content == "subreddit":
        return build_subreddit_reply(command.subreddit, command.page, command.sort, command.time)
    elif command.content == "post":
        return build_post_reply(command.post_id)
    elif command.content == "comments":
        return build_comment_reply(command.post_id, command.page, command.sort)
    else:
        return None, None


def build_subreddit_reply(sub: str, page: int, sort: str, time: str) -> tuple[list[str], list[dict]]:
    posts = reddit.list_posts(sub, page, sort, time)

    if posts.items:
        display_names = [
            f"Title: {post.title} | ID: {post.id} | /r/{post.subreddit.display_name} | /u/{post.author.name} | {post.score}pts | {post.num_comments}cmnts"
            for post in posts.items
        ]

        header = [f"Subreddit: /r/{sub.title()} | Page: {page}"]
        messages = header + (display_names or [f"No more posts :'("])

        return messages , None
    else:
        return [f"Error: {sub} is not a sub or Reddit is having issues :'("], None


def build_post_reply(post_id: str) -> tuple[list[str], list[dict]]:
    post = reddit.get_post(post_id)
    if post:
        header = [f"Title: {post.title} | ID: {post.id} | /r/{post.subreddit.display_name} | /u/{post.author.name} | {post.score}pts | {post.num_comments}cmnts"]
        messages = header + ([post.selftext] if post.selftext else ["No post body or this is an image post :'("])
        return messages, None
    else:
        return [f"Error: {post_id} is not a valid post ID or Reddit is having issues :'("], None


def build_comment_reply(post_id: str, page: int, sort: str) -> tuple[list[str], list[dict]]:
    post = reddit.get_post(post_id)
    post_comments = reddit.get_post_comments(post_id, page, sort)
    if post and post_comments.items:
        header = [f"Title: {post.title} | ID: {post.id} | /r/{post.subreddit.display_name} | /u/{post.author.name} | {post.score}pts | {post.num_comments}cmnts"]
        comments = [f"/u/{comment.author} | {comment.score}pts: {comment.body}" for comment in post_comments.items]
        messages = header + (comments or ["No more comments :'("])
        return messages, None
    else:
        return [f"Error: {post_id} is not a valid post ID or Reddit is having issues :'("], None
