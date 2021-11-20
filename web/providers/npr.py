from web.providers.provider import Provider


class Npr(Provider):
    def get_articles(self) -> str:
        return "No news today."

    def get_article(self, article: int) -> str:
        return f"The government deleted article {article}, sorry :)"