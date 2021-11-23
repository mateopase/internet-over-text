from argparse import Namespace

from bot.providers import reddit


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
            f"*{post.title}* | /r/{post.subreddit.display_name} | ID: {post.id} | _{post.score}pts, {post.num_comments}cmnts_"
            for post in posts.items
        ]

        header = [f"*Subreddit: /r/{sub.title()}* | _Pg. {page}_"]
        messages = header + (display_names or [f"No more posts :'("])
        buttons = [
            {
                "content_type": "text",
                "title": post.title,
                "payload": f"reddit post {post.id}",
            } 
        for post in posts.items]
        if page != 1:
            buttons += [{
                "content_type": "text",
                "title": "Previous Page",
                "payload": f"reddit subreddit {sub} -p {page} -s {sort} -t {time}",
            }]
        if posts.has_more:
            next_page = page + 1
            buttons += [{
                "content_type": "text",
                "title": "Next Page",
                "payload": f"reddit subreddit {sub} -p {next_page} -s {sort} -t {time}",
            }]

        return messages, buttons
    else:
        return [f"*Error:* {sub} is not a sub or Reddit is having issues :'("], None


def build_post_reply(post_id: str) -> tuple[list[str], list[dict]]:
    post = reddit.get_post(post_id)
    if post:
        header = [f"*{post.title}* | /r/{post.subreddit.display_name} | ID: {post.id} | _{post.score}pts, {post.num_comments}cmnts_"]
        messages = header + ([post.selftext] if post.selftext else ["No post body or this is an image post :'("])
        buttons = [
            {
                "content_type": "text",
                "title": f"Back to posts (hot)",
                "payload": f"reddit subreddit {post.subreddit.display_name}",
            },
            {
                "content_type": "text",
                "title": f"Load comments",
                "payload": f"reddit comments {post_id}",
            }
        ]
        return messages, buttons
    else:
        return [f"*Error:* {post_id} is not a valid post ID or Reddit is having issues :'("], None


def build_comment_reply(post_id: str, page: int, sort: str) -> tuple[list[str], list[dict]]:
    post = reddit.get_post(post_id)
    post_comments = reddit.get_post_comments(post_id, page, sort)
    if post and post_comments.items:
        header = [f"*{post.title}* | /r/{post.subreddit.display_name} | ID: {post.id} | _{post.score}pts, {post.num_comments}cmnts_"]
        comments = [f"*/u/{comment.author} | {comment.score}pts:* {comment.body}" for comment in post_comments.items]
        messages = header + (comments or ["No more comments :'("])
        buttons = [
            {
                "content_type": "text",
                "title": f"Back to post",
                "payload": f"reddit post {post.id}",
            } 
        ]

        if page != 1:
            buttons += [{
                "content_type": "text",
                "title": "Previous page",
                "payload": f"reddit comments {post_id} -p {page} -s {sort}",
            }]
        if post_comments.has_more:
            next_page = page + 1
            buttons += [{
                "content_type": "text",
                "title": "Next page",
                "payload": f"reddit comments {post_id} -p {next_page} -s {sort}",
            }]
        return messages, buttons
    else:
        return [f"*Error:* {post_id} is not a valid post ID or Reddit is having issues :'("], None
