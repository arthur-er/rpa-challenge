import re
from dataclasses import dataclass
from typing import Union


@dataclass
class Article:
    """
    A class to represent an article with additional metadata.

    Args:
        title: The title of the article.
        date: The publication date of the article.
        description: The description of the article.
        search_phrase: The search phrase used to find the article.
        thumbnail: The thumbnail image URL of the article, or None if not available.
    """
    title: Union[str, None]
    date: Union[str, None]
    description: Union[str, None]
    mentions_money: bool
    search_phrase_count: int
    thumbnail: Union[str, None]

    def __init__(self, title, date, description, search_phrase, thumbnail) -> None:
        """
        Initialize the Article with the provided title, date, description, search phrase, and thumbnail.

        Args:
            title: The title of the article.
            date: The publication date of the article.
            description: The description of the article.
            search_phrase: The search phrase used to find the article.
            thumbnail: The thumbnail image URL of the article, or None if not available.

        Returns:
            None
        """
        self.title = title
        self.date = date
        self.description = description
        self.thumbnail = thumbnail
        self.search_phrase_count = self.count_search_phrases_in_article(
            search_phrase)
        self.mentions_money = self.mentions_money_in_article()

    def mentions_money_in_article(self) -> bool:
        """
        Check if the article mentions money in the title or description.

        Args:
            None

        Returns:
            bool: True if money is mentioned, False otherwise.

        Raises:
            None
        """
        pattern = r'\$(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)|\b(\d+)\s*(?:dollars|USD)\b'
        results = re.search(pattern, self.title) or re.search(
            pattern, self.description)
        return results is not None

    def count_search_phrases_in_article(self, search_phrase: str) -> int:
        """
        Count the occurrences of the search phrase in the title and description of the article.

        Args:
            search_phrase: The search phrase to count in the article.

        Returns:
            int: The total count of the search phrase in the title and description.

        Raises:
            None
        """
        title_search_phrase_count = self.title.count(
            search_phrase) if self.title else 0
        description_search_phrase_count = self.description.count(
            search_phrase) if self.description else 0

        return title_search_phrase_count + description_search_phrase_count
