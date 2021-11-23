import praw
from praw.models import Submission, Comment

from bot.utils.settings import (
    REDDIT_CLIENT_ID,
    REDDIT_CLIENT_SECRET
)
from .models import Page


USER_AGENT = "python:com.internet-over-text.reddit:v0 (by /u/internet-over-text)"
PAGE_SIZE = 10


# TODO: Actually handle errors in this class
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
            sub = self.reddit.subreddit(subreddit)
            sub.name
            return sub

    def list_posts(self, subreddit: str, page: int, sort: str, time: str) -> Page[Submission]:
        post_limit = page * PAGE_SIZE

        try:
            if sort == "top":
                # Grab one extra post to see if there are more pages
                posts = list(self._get_subreddit(subreddit).top(time, limit=1+post_limit))
            elif sort == "new":
                posts = list(self._get_subreddit(subreddit).new(limit=1+post_limit))
            else:  # hot
                posts = list(self._get_subreddit(subreddit).hot(limit=1+post_limit))
        except:
            return Page(None, False)

        post_page = posts[post_limit - 10: post_limit]
        has_more = len(posts) > post_limit

        # There's at least one more page if we were able to load the extra comment
        return Page(post_page, has_more)

    def get_post(self, post_id: str) -> Submission:
        try:
            submission = self.reddit.submission(id=post_id) 
            submission.title
            return submission
        except:
            return None

    def get_post_comments(self, post_id: int, page: int, sort: str) -> Page[Comment]:
        post = self.get_post(post_id)
        if post:
            post.comment_sort = sort

            comment_limit = page * PAGE_SIZE

            comments = post.comments[comment_limit - 10: 1+comment_limit]
            comments = list(filter(lambda c: isinstance(c, Comment), comments))
            comment_page = comments[:-1]

            return Page(comment_page, len(comments) > PAGE_SIZE)
        return Page(None, False)