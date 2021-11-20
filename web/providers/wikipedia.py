from web.providers.provider import Provider


class Wikipedia(Provider):
    def get_article(self, article: str) -> str:
        return f"I can't find {article} :("