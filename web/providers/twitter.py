from web.providers.provider import Provider


class Twitter(Provider):
    def get_user_posts(self, user: str) -> str:
        return f"{user} I miss you :'("