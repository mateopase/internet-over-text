from web.providers.provider import Provider


class Reddit(Provider):
    def get_subreddit_posts(self, subreddit: str) -> str:
        return f"subreddit: {subreddit}"

    def get_post(self, subreddit: str, post: int) -> str:
        return f"subreddit: {subreddit} and post: {post}"