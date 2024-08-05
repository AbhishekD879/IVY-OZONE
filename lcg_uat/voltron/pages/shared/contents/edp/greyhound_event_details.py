from collections import OrderedDict

from selenium.common.exceptions import StaleElementReferenceException
from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.pages.shared.components.primitives.buttons import IconBase
from voltron.pages.shared.components.primitives.text_labels import TextBase
from voltron.pages.shared.contents.base_contents.racing_base_components.each_way_terms import EachWayTerms
from voltron.pages.shared.contents.edp.racing_edp_market_section import ExpandedSummary
from voltron.pages.shared.contents.edp.racing_edp_market_section import ForecastTricastButtons
from voltron.pages.shared.contents.edp.racing_edp_market_section import Outcome
from voltron.pages.shared.contents.edp.racing_edp_market_section import RacingMarketSection
from voltron.pages.shared.contents.edp.racing_edp_market_section import SummaryText
from voltron.pages.shared.contents.edp.racing_event_details import EventMarketsList
from voltron.pages.shared.contents.edp.racing_event_details import PostInfo
from voltron.pages.shared.contents.edp.racing_event_details import RacingEDPTabContent
from voltron.pages.shared.contents.edp.racing_event_details import RacingEventDetails
from voltron.pages.shared.contents.edp.racing_event_details import SubHeader
from voltron.utils.waiters import wait_for_result


class Rating(ComponentBase):
    _item = 'xpath=.//*[@data-crlat="value"]'
    _list_item_type = IconBase
    _label = 'xpath=.//*[@data-crlat="label"]'

    @property
    def label(self):
        return self._get_webelement_text(selector=self._label, timeout=0.5)

    @property
    def items_as_ordered_dict(self) -> OrderedDict:
        items_we = self._find_elements_by_selector(selector=self._item, context=self._we)
        self._logger.debug(f'*** Found {len(items_we)} {self.__class__.__name__} - {self._list_item_type.__name__} items')
        items_ordered_dict = OrderedDict()
        for index, item_we in enumerate(items_we):
            items_ordered_dict[index] = item_we
        return items_ordered_dict


class DogPositionEntry(ComponentBase):
    _name = 'xpath=.//*[@data-crlat="greyhoundName"] | .//*[contains(@class, "greyhound-name")]/span[1]'
    _trainer_name = 'xpath=.//*[@data-crlat="greyhoundTrainer"] | .//*[text()="Trainer"]/following-sibling::b'
    _trainer_label = 'xpath=.//*[@data-crlat="greyhoundTrainer.label"] | .//*[contains(@class, "greyhound-name")]//b'
    _logo = 'xpath=.//*[local-name()="svg"][@data-crlat="position.logo"] | .//*[contains(@class, "position-logo position")]'
    _rating_container = 'xpath=.//*[@data-crlat="greyhoundRating"]'

    @property
    def name(self):
        return self._get_webelement_text(selector=self._name, timeout=0.5)

    @property
    def trainer_name(self):
        return self._get_webelement_text(selector=self._trainer_name, timeout=0.5)

    @property
    def trainer_label(self):
        return self._get_webelement_text(selector=self._trainer_label, timeout=0.5)

    def has_logo(self, timeout=1, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._logo,
                                                   timeout=0) is not None,
            name=f'Logo status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)

    def has_rating(self, timeout=1, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._rating_container,
                                                   timeout=0) is not None,
            name=f'Rating status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)

    @property
    def rating(self):
        return Rating(selector=self._rating_container, context=self._we)

    @property
    def stars_count(self):
        return len(self.rating.items_as_ordered_dict)


class TimeformPositions(ComponentBase):
    _item = 'xpath=.//*[@data-crlat="position.greyhound"] | .//*[contains(@class, "greyhound-details")]'
    _list_item_type = DogPositionEntry


class TimeformOverview(PostInfo):
    _show_summary_btn = 'xpath=.//*[@data-crlat="timeform.showSummary"]'
    _summary_text = 'xpath=.//*[@data-crlat="timeform.text"]'
    _logo_icon = 'xpath=.//*[local-name()="svg"][@data-crlat="timeform.logo"]'
    _prediction = 'xpath=.//*[@data-crlat="timeformPrediction"] | .//*[contains(@class, "timeform-prediction")]/span'
    _positions = 'xpath=.//*[@data-crlat="timeformPositions"] | .//*[contains(@class, "timeform-widget-positions")]'
    _prediction_value = 'xpath=.//*[contains(@class, "timeform-prediction")]/span[2]'

    @property
    def show_summary_button(self):
        return ButtonBase(selector=self._show_summary_btn, context=self._we)

    @property
    def logo_icon(self):
        return ComponentBase(selector=self._logo_icon)

    @property
    def summary_text(self):
        return SummaryText(selector=self._summary_text, context=self._we)

    @property
    def prediction(self):
        return TextBase(selector=self._prediction, context=self._we)

    @property
    def prediction_value(self):
        return TextBase(selector=self._prediction_value, context=self._we)

    def has_prediction(self, timeout=1, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._prediction,
                                                   timeout=0) is not None,
            name=f'Prediction status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)

    def has_positions(self, timeout=1, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._positions,
                                                   timeout=0) is not None,
            name=f'Position status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)

    @property
    def positions(self):
        return TimeformPositions(selector=self._positions, context=self._we)

    def is_expanded(self, timeout=1, expected_result=True, bypass_exceptions=(StaleElementReferenceException, )):
        we = self._find_element_by_selector(selector='xpath=.//*[@data-crlat="accordion"]', timeout=timeout)

        result = wait_for_result(lambda: 'is-expanded' in we.get_attribute('class'),
                                 name=f'"{self.__class__.__name__}" Accordion to expand',
                                 expected_result=expected_result,
                                 bypass_exceptions=bypass_exceptions,
                                 timeout=timeout)
        result = result if result else False
        self._logger.debug(f'*** "{self.__class__.__name__}" Accordion expanded status is "{result}"')
        return result


class GreyhoundExpandedSummary(ExpandedSummary):
    _rating_container = 'xpath=.//*[@data-crlat="greyhoundRating"]'
    _outcome_overview = 'xpath=.//*[@data-crlat="timeform.text"]'

    @property
    def rating(self):
        return Rating(selector=self._rating_container, context=self._we)

    @property
    def stars_count(self):
        return len(self.rating.items_as_ordered_dict)


class GreyhoundOutcome(Outcome):
    _trainer_name = 'xpath=.//*[@data-crlat="trainerName"] | .//*[@class="timeform-trainer"]/span'
    _label_name = 'xpath=.//*[@class="timeform-trainer"]/strong | .//*[@data-crlat="jockeyAndTrainer"]/span'
    _form_value = 'xpath=.//*[@data-crlat="racingForm"]/strong | .//*[contains(@class,"racing-form")]/span/span'
    _expanded_summary = 'xpath=.//*[@data-crlat="timeform.selectionSummary"] | .//*[@data-crlat="spotlight" or @data-crlat="runnerSpotlight"]'
    _silks = 'xpath=.//*[@data-crlat="gh-silk"]'
    _expanded_summary_type = GreyhoundExpandedSummary

    @property
    def trainer_name(self):
        return TextBase(selector=self._trainer_name, context=self._we)

    @property
    def is_non_runner(self):
        return 'N/R' in self.horse_name

    @property
    def trainer_label(self):
        return TextBase(selector=self._label_name, context=self._we)

    @property
    def form_value(self):
        return TextBase(selector=self._form_value, context=self._we)


class GreyhoundMarketSection(RacingMarketSection):
    _cash_out_label = 'xpath=.//*[@data-crlat="labelCashout"]'
    _bpg_icon = 'xpath=.//*[@data-crlat="bogIcon"]'
    _ew_terms = 'xpath=.//*[@data-crlat="terms" or @data-crlat="eachWayContainer"]'
    _forecast_tricast = 'xpath=.//*[@data-crlat="raceCard.forTri"]'

    @property
    def _list_item_type(self):
        is_forecast_tricast = self._find_element_by_selector(selector=self._forecast_tricast, timeout=0)
        if is_forecast_tricast:
            return ForecastTricastButtons
        return GreyhoundOutcome

    def is_bpg_icon_present(self, expected_result=True, timeout=3):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._bpg_icon, timeout=0),
                               expected_result=expected_result,
                               timeout=timeout,
                               name=f'BPG icon presence status to be "{expected_result}"')

    def has_cashout_label(self, expected_result=True, timeout=3):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._cash_out_label, timeout=0),
                               expected_result=expected_result,
                               timeout=timeout,
                               name=f'Cashout label presence status to be "{expected_result}"')

    @property
    def each_way_terms(self):
        return EachWayTerms(selector=self._ew_terms, context=self._we)

    @property
    def has_each_way_terms(self):
        return self._find_element_by_selector(selector=self._ew_terms, timeout=1) is not None


class GreyhoundEventMarketsList(EventMarketsList):
    _forecast_tricast = 'xpath=.//*[@data-crlat="raceCard.forTri"]'

    @property
    def _list_item_type(self):
        is_forecast_tricast = self._find_element_by_selector(selector=self._forecast_tricast, timeout=0)
        if is_forecast_tricast:
            return RacingMarketSection
        return GreyhoundMarketSection


class GreyHoundSubHeader(SubHeader):
    _meeting_selector = 'xpath=.//*[@data-crlat="meetingSelector"]'

    @property
    def event_name(self):
        return NotImplementedError('There\'s no event name in sub header for Greyhound EDP')


class GreyHoundEDPTabContent(RacingEDPTabContent):
    _event_markets_list_type = GreyhoundEventMarketsList
    _status = 'xpath=.//*[@data-crlat="raceGrade"]'
    _timeform_container = 'xpath=.//*[@data-crlat="timeformContainer"]'

    def has_timeform_overview(self, timeout=2, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._timeform_container,
                                                   timeout=0) is not None,
            name=f'Timeform status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)

    def has_grade(self, timeout=1, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._status,
                                                   timeout=0) is not None,
            name=f'Timeform status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)

    @property
    def grade(self):
        return TextBase(selector=self._status, context=self._we)

    @property
    def timeform_overview(self):
        return TimeformOverview(selector=self._timeform_container, context=self._we)


class GreyHoundEventDetails(RacingEventDetails):
    _tab_content_type = GreyHoundEDPTabContent
    _url_pattern = r'^http[s]?:\/\/.+\/(greyhound-racing)\/[\w-]+\/[\w-]+\/[\w-]+\/[0-9]+\/[\w-]+'
    _sub_header_type = GreyHoundSubHeader

    @property
    def event_name(self):
        return self.event_title
