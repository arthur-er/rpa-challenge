from datetime import datetime
from typing import List
from dotenv import load_dotenv
from os import getenv
from RPA.Robocorp.WorkItems import WorkItems
from dateutil.relativedelta import relativedelta

load_dotenv()

env = getenv('ENV', 'production')


class RobotConfig:
    search_phrase: str = None
    sections: List[str] = None
    months: int = None
    start_date: datetime = None
    end_date: datetime = datetime.today()
    output_file: str = None

    def __init__(self) -> None:
        if env == 'production':
            self.setup_with_workitems()
        else:
            self.setup_with_env()

        self.months = 1 if self.months == 0 else self.months
        self.start_date = datetime.today() - relativedelta(months=self.months)

    def setup_with_workitems(self):
        work_items = WorkItems()
        work_items.get_input_work_item()
        self.search_phrase = work_items.get_work_item_variable(
            'SEARCH_PHRASE', 'Airport')
        self.sections = self.normalize_categories(
            work_items.get_work_item_variable('SECTIONS', 'World'))
        self.months = int(work_items.get_work_item_variable('MONTHS', 2))
        self.output_file = work_items.get_work_item_variable(
            'OUTPUT_FILE', 'output')

    def setup_with_env(self):
        self.search_phrase = getenv('SEARCH_PHRASE', 'Airport')
        self.sections = self.normalize_categories(
            getenv('SECTIONS', 'World'))
        self.months = int(getenv('MONTHS', 2))
        self.output_file = getenv('OUTPUT_FILE', 'output')

    def normalize_categories(self, categories_string: str):
        return [category.strip() for category in categories_string.split(',')]
