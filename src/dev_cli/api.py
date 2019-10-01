from typing import Dict, Iterator, Optional, Text

from httpx import Client

from .errors import DevApiError
from .parser import DevKey, DevParser


class DevApi:
    """
    A class to access the dev.to API
    """

    BASE_URL = "https://dev.to/api"

    def __init__(self, api_key: Text):
        """
        Creates the HTTP client
        """

        self.api_key = api_key
        self.client = Client(headers=[("Api-Key", self.api_key)])

    def url(self, path: Text) -> Text:
        """
        Generates an URL, be careful not to put any slash at the start or the
        end.
        """

        return f"{self.BASE_URL}/{path}"

    def get_my_articles(self, publication: Text = "all") -> Iterator[Dict]:
        """
        Returns an iterator over all the articles corresponding to the
        publication filter.

        :param publication: Publication status. Allowed values are "published",
                            "unpublished" and "all"
        :return: An iterator of all selected articles
        """

        assert publication in {"published", "unpublished", "all"}

        url = self.url(f"articles/me/{publication}")

        class NoMorePages(Exception):
            """
            A way to communicate that there is no more page coming up from the
            API and that the polling of pages should stop now.
            """

        def get_page(page: int):
            """
            Returns a given page. Pages are 1-indexed.
            """

            r = self.client.get(url, params={"page": page})
            stop = True

            for article in r.json():
                stop = False
                yield article

            if stop:
                raise NoMorePages

        for i in range(1, 1000):
            try:
                yield from get_page(i)
            except NoMorePages:
                return

    def find_article(self, key: DevKey) -> Optional[Dict]:
        """
        Finds the first article matching they key. Let's take a moment to note
        that this method is really approximate but since we can't retrofit the
        API ID into the Markdown file it's the only decent way to go.
        """

        for article in self.get_my_articles():
            if article[key.name] == key.value:
                return article

    def create_article(self, parser: DevParser) -> None:
        """
        Creates an article based on the parsed file.
        """

        url = self.url("articles")

        if "title" not in parser.front_matter:
            raise DevApiError(
                "Cannot create an article with no `title` in the front matter"
            )

        r = self.client.post(
            url,
            json={
                "title": parser.front_matter["title"],
                "body_markdown": parser.file_content,
            },
        )
        r.raise_for_status()

    def update_article(self, parser: DevParser, article_id: int) -> None:
        """
        Updates an article based on the parsed file and an existing ID.
        """

        url = self.url(f"articles/{article_id}")

        r = self.client.put(url, json={"body_markdown": parser.file_content})
        r.raise_for_status()
