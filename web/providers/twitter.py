from web.providers.provider import Provider


class Twitter(Provider):
    def get_posts(user: str) -> str:
        return f"{user} I miss you :'("