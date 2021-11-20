import os

import praw

from web.providers.provider import Provider


USER_AGENT = "python:com.internet-over-text.reddit:v0 (by /u/internet-over-text)"

class Reddit(Provider):
    reddit = praw.Reddit(
        client_id=os.environ.get("REDDIT_CLIENT_ID"),
        client_secret=os.environ.get("REDDIT_CLIENT_SECRET"),
        user_agent=USER_AGENT,
    )

    def get_subreddit(self, subreddit: str) -> str:
        posts = self.reddit.subreddit(subreddit).hot(limit=10)
        titles = [f"[{num}] {post.title} | {post.subreddit.display_name}" for num, post in enumerate(posts, start=1)]
        return "\n".join(titles)

    def get_post(self, subreddit: str, post: int) -> str:
        posts = self.reddit.subreddit(subreddit).hot(limit=10)
        return list(posts)[post - 1].selftext
