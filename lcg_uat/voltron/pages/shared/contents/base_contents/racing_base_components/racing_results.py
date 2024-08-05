import re

from voltron.pages.shared.components.fixture_header import FixtureHeader
from voltron.pages.shared.contents.base_contents.common_base_components.event_group import EventGroup
from voltron.pages.shared.contents.base_contents.racing_base_components.each_way_terms import EachWayRacingResults
from voltron.pages.shared.components.accordions_container import Accordion
from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.primitives.text_labels import TextBase
from voltron.utils.waiters import wait_for_result
from voltron.pages.shared.contents.edp.racing_edp_market_section import Outcome as RacingOutcome


class Outcome(ComponentBase):
    _place = 'xpath=.//*[@data-crlat="racingTabResults.outcomePosition"]'
    _favourite_icon = 'xpath=.//*[@data-crlat="racingTabResults.favourite"]'
    _name = 'xpath=.//*[@data-crlat="racingTabResults.outcomeName"]'
    _price = 'xpath=.//*[@data-crlat="racingTabResults.outcomePrice"]'
    _silk = 'xpath=.//*[@data-crlat="racingTabResults.outcomeSilk"]'
    _jockey_trainer = 'xpath=.//*[@data-crlat="racingTabResults.jockeyAndTrainerName"]'

    @property
    def favorite_icon(self):
        return self._get_webelement_text(selector=self._favourite_icon, context=self._we, timeout=1)

    def has_favourite_icon(self, timeout=1, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._favourite_icon, timeout=0) is not None,
            name=f'{self.__class__.__name__} Favourite Icon status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)

    @property
    def place(self):
        return self._get_webelement_text(selector=self._place, context=self._we)

    @property
    def name(self):
        return self.outcome_name.name

    @property
    def outcome_name(self):
        return TextBase(selector=self._name, context=self._we)

    @property
    def price(self):
        return TextBase(selector=self._price, context=self._we)

    @property
    def price_text(self):
        return self.price.name

    @property
    def jockey_trainer(self):
        return self._get_webelement_text(selector=self._jockey_trainer, context=self._we)

    @property
    def has_silks(self):
        return self._find_element_by_selector(selector=self._silk, timeout=0) is not None


class ResultTable(Accordion):
    _item = 'xpath=.//*[@data-crlat="racingTabResults.outcome"]'
    _list_item_type = Outcome
    _ew_container = 'xpath=.//*[@data-crlat="racingTabResults.outcome.ew"]'
    _small_header = 'xpath=.//*[@data-crlat="racingTabResults.byMeetings.event.offTime" or @data-crlat="headerTitle.centerMessage"]'
    _name = 'xpath=.//*[@data-crlat="racingTabResults.byMeetings.event.offTime"]'
    _fixture_header = 'xpath=.//*[@data-crlat="eventOddsHeader"]'
    _header_type = FixtureHeader

    @property
    def fixture_header(self):
        return self._header_type(selector=self._fixture_header, context=self._we)

    @property
    def name(self):
        return TextBase(selector=self._name, context=self._we).name

    @property
    def has_each_way_terms(self):
        return self.each_way_terms.odds and self.each_way_terms.places is not None

    @property
    def each_way_terms(self):
        return EachWayRacingResults(selector=self._ew_container, context=self._we)

    @property
    def off_time(self):
        text = self._get_webelement_text(selector=self._small_header, timeout=2)
        find = re.search(r'([:\d]+)', text)
        return find.group(0) if find else ''

    @property
    def event_name(self):
        return self.off_time


class ResultsByLatestResult(EventGroup):
    _name = 'xpath=.//*[@data-crlat="headerTitle.centerMessage"]'
    _result_table = 'xpath=.//*[@data-crlat="race.racingTabResults.byLatest.results"]'

    @property
    def result_table(self):
        return ResultTable(selector=self._result_table, context=self._we)

    @property
    def name(self):
        return TextBase(selector=self._name, context=self._we).name


class ResultsByMeeting(EventGroup):
    _item = 'xpath=.//*[@data-crlat="race.racingTabResults.byMeetings.event"]'
    _name = 'xpath=.//*[@data-crlat="headerTitle.centerMessage"]'
    _list_item_type = ResultTable

    @property
    def name(self):
        return TextBase(selector=self._name, context=self._we).name


class EachOutcome(RacingOutcome):
    _place_rank = 'xpath=.//*[@class="odds-side"]'
    _odds_price = 'xpath=.//*[@class="odds-right"]'

    @property
    def place_rank(self):
        return self._find_element_by_selector(selector=self._place_rank, timeout=2)

    @property
    def odds_price(self):
        return self._find_element_by_selector(selector=self._odds_price, timeout=2)


class HorseRacingResultedEventsPage(EventGroup):
    _each_way_container = 'xpath=.//*[@data-crlat="eachWayContainer"]'
    _item = 'xpath=.//*[@class="section-container"]//div[@data-crlat="outcomeEntity"]'
    _list_item_type = EachOutcome
    _meeting_name = 'xpath=.//*[@class="race-event-name"]'
    _event_day_date = 'xpath=.//*[@data-crlat="raceGoing"]'

    @property
    def meeting_name(self):
        return self._get_webelement_text(selector=self._meeting_name, timeout=2)

    @property
    def event_day_date(self):
        return self._get_webelement_text(selector=self._event_day_date, timeout=2)

    @property
    def each_way_container(self):
        return self._find_element_by_selector(selector=self._each_way_container, timeout=2)


class TriForecast(EventGroup):
    _name_col = 'xpath=.//*[@class="name-col"]'
    _result_col = 'xpath=.//*[@class="dividend-result-col"]'
    _value_col = 'xpath=.//*[@class="value-col"]'

    @property
    def name_col(self):
        return self._find_element_by_selector(selector=self._name_col, timeout=1)

    @property
    def result_col(self):
        return self._find_element_by_selector(selector=self._result_col, timeout=1)

    @property
    def value_col(self):
        return self._find_element_by_selector(selector=self._value_col, timeout=1)


class HorseRacingTriForecast(EventGroup):
    _item = 'xpath=.//*[@class="section-container dividends space-top"]//div[@class="result-card"]'
    _list_item_type = TriForecast


class RacingHeaders(EventGroup):
    _headers = 'xpath=.//*[contains(@class, "section-header")]'

    @property
    def headers(self):
        return self._find_element_by_selector(selector=self._headers, timeout=2)
