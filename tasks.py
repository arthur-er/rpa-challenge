from dataclasses import asdict
from pathlib import Path
from pandas import DataFrame
from RPA.Browser.Selenium import Selenium
from robocorp.tasks import task
from loguru import logger as log
from selenium.webdriver.chrome.options import Options

from config.robot import RobotConfig
from robots.new_york_times import NewYorkTimesRobot


@task
def scrape_articles():
    try:
        log.info('Creating thumbnails folder')
        Path('output/thumbnails').mkdir(parents=True, exist_ok=True)

        log.info('Configuring browser')
        browser_options = Options()
        browser_options.add_argument("--no-sandbox")
        browser_options.add_argument("--disable-dev-shm-usage")
        browser = Selenium()

        log.info('Loading config')
        config = RobotConfig()

        log.info('Starting Robot')
        robot = NewYorkTimesRobot(browser, browser_options, config)
        articles = robot.run()

        log.info('Exporting CSV')
        dataframe = DataFrame([asdict(article) for article in articles])
        dataframe.to_csv(f'output/{config.output_file}.csv', index=False)
        log.info(
            f"Exported {len(articles)} articles to {config.output_file}.csv")

    finally:
        log.info("Automation finished!")
