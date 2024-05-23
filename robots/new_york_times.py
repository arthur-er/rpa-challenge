from datetime import date
from time import sleep
from typing import List
from RPA.Browser.Selenium import Selenium, By
from selenium.webdriver.chrome.options import Options
from loguru import logger as log
import requests

from config.robot import RobotConfig
from models.article import Article

nytimes_url = 'https://www.nytimes.com/'
accept_cookies_button_locator = '//button[@data-testid="Accept all-btn"]'
sections_button_locator = '//div[@data-testid="section"]//button[@data-testid="search-multiselect-button"]'
article_locator = '//li[@data-testid="search-bodega-result"]'
article_title_class = 'css-nsjm9t'
article_description_class = 'css-16nhkrn'
article_date_class = 'css-17ubb9w'
article_thumbnail_class = 'css-rq4mmj'


class NewYorkTimesRobot:
    def __init__(self, browser: Selenium, browser_options: Options, config: RobotConfig) -> None:
        self.browser = browser
        self.browser_options = browser_options
        self.config = config

        start_date = config.start_date.strftime('%Y-%m-%d')
        end_date = config.end_date.strftime('%Y-%m-%d')

        self.search_url = f"{nytimes_url}/search?query={config.search_phrase}&sort=newest&startDate={start_date}&endDate={end_date}"

    def open(self):
        self.browser.open_available_browser(
            url=self.search_url,
            headless=False,
            maximized=True,
            options=self.browser_options,
            browser_selection='Chrome'
        )

    def accept_cookies(self):
        self.browser.click_button_when_visible(
            '//button[@data-testid="Accept all-btn"]')

    def select_sections(self):
        # open the sections dropdown
        self.browser.click_button_when_visible(sections_button_locator)

        # select the applicable sections
        for section in self.config.sections:
            section_locator = f'//input[contains(@value, "{section}")]'
            self.browser.click_element_if_visible(section_locator)

        # close the sections dropdown
        self.browser.click_button_when_visible(sections_button_locator)

    def download_thumbnail(self, article_element):
        try:
            thumbnail = article_element.find_element(
                By.CLASS_NAME, article_thumbnail_class).get_attribute('src')
            thumbnail_url = thumbnail.split('?')[0]
            thumbnail_filename = thumbnail_url.split('/')[-1]
            with open(f'output/{thumbnail_filename}', 'wb') as file:
                file.write(requests.get(thumbnail_url).content)
            return thumbnail_filename
        except Exception:
            log.error("Thumbnail not found")
            return None

    def get_article_title(self, article_element):
        try:
            title = article_element.find_element(
                By.CLASS_NAME, article_title_class).text
            return title
        except Exception:
            log.error("Title not found")
            return ''

    def get_article_description(self, article_element):
        try:
            description = article_element.find_element(
                By.CLASS_NAME, article_description_class).text
            return description
        except Exception:
            log.error("Description not found")
            return ''

    def get_article_date(self, article_element):
        try:
            description = article_element.find_element(
                By.CLASS_NAME, article_description_class).text
            return description
        except Exception:
            log.error("Date not found")
            return ''

    def scrape_articles(self) -> List[Article]:
        self.browser.wait_until_element_is_visible(article_locator)

        articles = []
        article_elements = self.browser.get_webelements(article_locator)

        for article_element in article_elements:
            title = self.get_article_title(article_element)
            date = self.get_article_date(article_element)
            description = self.get_article_description(article_element)
            thumbnail = self.download_thumbnail(article_element)

            article = Article(
                title=title,
                description=description,
                date=date,
                search_phrase=self.config.search_phrase,
                thumbnail=thumbnail
            )

            articles.append(article)

        return articles

    def run(self):
        self.open()
        self.accept_cookies()
        self.select_sections()

        sleep(5)  # wait for the articles to load

        articles = self.scrape_articles()

        self.browser.close_all_browsers()

        return articles
