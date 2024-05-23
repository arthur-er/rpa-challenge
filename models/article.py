import re
from dataclasses import dataclass
from typing import Union

@dataclass
class Article:
  title: str
  date: str
  description: str
  mentions_money: bool
  search_phrase_count: int
  thumbnail: Union[str, None]

  def __init__(self, title, date, description, search_phrase, thumbnail) -> None:
    self.title = title
    self.date = date
    self.description = description
    self.thumbnail = thumbnail
    self.search_phrase_count = self.count_search_phrases_in_article(search_phrase)
    self.mentions_money = self.mentions_money_in_article()

  def mentions_money_in_article(self):
    pattern =  r'\$(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)|\b(\d+)\s*(?:dollars|USD)\b'
    results = re.search(pattern, self.title) or re.search(pattern, self.description)
    return results is not None
  
  def count_search_phrases_in_article(self, search_phrase):
    title_search_phrase_count = self.title.count(search_phrase) if self.title else 0
    description_search_phrase_count = self.description.count(search_phrase) if self.description else 0

    return title_search_phrase_count + description_search_phrase_count