import praw
from praw.models import Submission, Comment

from bot.utils.settings import (
    REDDIT_CLIENT_ID,
    REDDIT_CLIENT_SECRET
)
from .models import Page


USER_AGENT = "python:com.internet-over-text.reddit:v0 (by /u/internet-over-text)"
PAGE_SIZE = 10



class Reddit:
    reddit = praw.Reddit(
        client_id=REDDIT_CLIENT_ID,
        client_secret=REDDIT_CLIENT_SECRET,
        user_agent=USER_AGENT,
    )

    def _get_subreddit(self, subreddit: str):
        if subreddit == "front":
            return self.reddit.front
        else:
            return self.reddit.subreddit(subreddit)

    def list_posts(self, subreddit: str, page: int, sort: str, time: str) -> Page[Submission]:
        post_limit = page * PAGE_SIZE

        if sort == "top":
            # Grab one extra post to see if there are more pages
            posts = list(self._get_subreddit(subreddit).top(time, limit=1+post_limit))
        elif sort == "new":
            posts = list(self._get_subreddit(subreddit).new(limit=1+post_limit))
        else:  # hot
            posts = list(self._get_subreddit(subreddit).hot(limit=1+post_limit))

        post_page = posts[post_limit - 10: post_limit]

        # There's at least one more page if we were able to load the extra comment
        return Page(post_page, len(posts) > post_limit)

    def get_post(self, post_id: str) -> Submission:
        return self.reddit.submission(id=post_id)

    def get_post_comments(self, post_id: int, page: int, sort: str) -> Page[Comment]:
        post = self.reddit.submission(id=post_id)
        post.comment_sort = sort

        comment_limit = page * PAGE_SIZE
        comments_to_load = min(comment_limit, post.num_comments)

        comment_page = post.comments[comment_limit - 10: comments_to_load]

        return Page(comment_page, post.num_comments > comment_limit and bool(comment_page))