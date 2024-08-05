import re

from voltron.pages.shared.components.primitives.selects import SelectBase
from voltron.pages.shared.components.primitives.text_labels import LinkBase
from voltron.pages.shared.contents.base_content import BaseContent
from voltron.pages.shared.contents.bet_filter.bet_filter_page import BetFilterPage
from voltron.pages.shared.contents.bet_filter.bet_filter_page import Filter
from voltron.pages.shared.contents.edp.racing_edp_market_section import Outcome
from voltron.pages.shared.components.primitives.text_labels import TextBase
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.waiters import wait_for_result


class HorseRacingBetFilterPage(BetFilterPage):
    _url_pattern = r'^http[s]?:\/\/.+\/bet-finder'

    FORM = ['COURSE AND DISTANCE WINNER', 'COURSE WINNER', 'DISTANCE WINNER', 'WINNER LAST TIME',
            'WINNER WITHIN LAST 3', 'PLACED LAST TIME', 'PLACED WITHIN LAST 3']
    ODDS = ['ODDS ON', 'EVENS - 7/2', '4/1 - 15/2', '8/1 - 14/1', '16/1 - 28/1', '33/1 OR BIGGER']

    DTF = ['SELECTION', 'ALTERNATIVE', 'EACH-WAY']  # DTF = Digital Tipster Filters

    _header_message = 'xpath=.//*[@data-crlat="headerMessage"]'

    _meetings_drop_down = 'xpath=.//*[@data-crlat="country"]'
    _stars_container = 'xpath=.//*[@data-crlat="bfStars"]'
    _stars = 'xpath=.//*[@data-crlat="stars"]'
    _fade_out_overlay = True

    _list_item_type = Filter

    @property
    def header_message(self):
        return TextBase(selector=self._header_message)

    @property
    def meetings_drop_down(self):
        return MeetingsDropDown(selector=self._meetings_drop_down, context=self._we)

    @property
    def stars_container(self):
        return self._find_element_by_selector(selector=self._stars_container)

    def set_stars_rating(self, rating):
        stars = self._find_elements_by_selector(selector=self._stars, context=self.stars_container)
        self.scroll_to_we(stars[0])
        stars[rating - 1].click()

    def get_star_rating(self):
        stars = self._find_elements_by_selector(selector=self._stars, context=self.stars_container)
        rating = len([star for star in stars if 'active' in star.get_attribute('class')])
        return rating

    @property
    def result_text(self):
        return self._get_webelement_text(selector=self._found_result_text, timeout=1)


class MeetingsDropDown(SelectBase):
    _options = 'xpath=.//option'

    def select_value(self, text):
        options = self._find_elements_by_selector(selector=self._options)
        for option in options:
            if option.text.title() == text:
                return option.click()

    def is_option_selected(self, option):
        return wait_for_result(lambda: self.selected_item == option,
                               name=f'Option "{option}" to be selected',
                               timeout=5)


class Runner(Outcome):
    _trainer_name = 'xpath=.//*[@data-crlat="trainerName"]'
    _form = 'xpath=.//*[@data-crlat="form"]'
    _time = 'xpath=.//*[@data-crlat="time"]'
    _course = 'xpath=.//*[@data-crlat="course"]'
    _odds = 'xpath=.//*[@data-crlat="odds"]'  # Note: not displayed for connect
    _runner_number = 'xpath=.//*[@data-crlat="number"]'
    _silks = 'xpath=.//*[@data-crlat="silk"]'
    _horse_name = 'xpath=.//*[@data-crlat="horseName"]'
    _jockey_name = 'xpath=.//*[@data-crlat="jockeyName"]'

    @property
    def silk(self):
        return self._find_element_by_selector(selector=self._silks, context=self._we)

    @property
    def horse_name(self):
        return self._find_element_by_selector(self._horse_name, context=self._we)

    @property
    def jockey_name(self):
        return self._find_element_by_selector(self._jockey_name, context=self._we)

    @property
    def runner_number(self):
        return self._find_element_by_selector(selector=self._runner_number, context=self._we)

    @property
    def trainer_name(self):
        return self._find_element_by_selector(selector=self._trainer_name, context=self._we)

    @property
    def form(self):
        return self._find_element_by_selector(selector=self._form, context=self._we)

    @property
    def time(self):
        return self._find_element_by_selector(selector=self._time, context=self._we)

    @property
    def course(self):
        return self._find_element_by_selector(selector=self._course, context=self._we)

    @property
    def odds(self):  # Note: not displayed for connect
        return self._find_element_by_selector(selector=self._odds, context=self._we)

    def get_odds_price(self, odds_text):
        if not odds_text:
            raise VoltronException(message='Odds text is empty')
        try:
            num, denom = odds_text.split('/')
        except ValueError:
            raise VoltronException(message=f'Odds text "{odds_text}" cannot be split by "/"')
        return float(num) / float(denom)


class HorseRacingBetFilterResultsPage(BaseContent):
    _url_pattern = r'^http[s]?:\/\/.+\/bet-finder\/results'

    TITLE = 'BET FILTER RESULTS'
    _number_of_results = 'xpath=.//*[@data-crlat = "resultsNumber"]'
    _time_sorting_link = 'xpath=.//*[@data-crlat = "sortByTime"]'
    _odds_sorting_link = 'xpath=.//*[@data-crlat = "sortByOdds"]'
    _item = 'xpath=.//*[@data-crlat = "runner"]'
    _list_item_type = Runner
    _verify_spinner = True

    @property
    def number_of_results(self):
        result = wait_for_result(lambda: self._find_element_by_selector(selector=self._number_of_results),
                                 name='Waiting non empty value', timeout=5)
        return int(re.findall(r'\d+', result.text)[0])

    @property
    def time_sorting_link(self):
        return LinkBase(selector=self._time_sorting_link, context=self._we, timeout=5)

    @property
    def odds_sorting_link(self):
        return LinkBase(selector=self._odds_sorting_link, context=self._we, timeout=5)
