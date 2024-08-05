from collections import OrderedDict

from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.pages.shared.components.uk_tote_bet_builder import UKToteBetBuilder
from voltron.pages.shared.contents.base_content import BaseContent
from voltron.pages.shared.contents.base_contents.common_base_components.tab_content import GroupingSelectionButtons
from voltron.pages.shared.contents.edp.racing_edp_market_section import Outcome
from voltron.pages.shared.contents.edp.racing_edp_market_section import RacingMarketSection
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.waiters import wait_for_result


class CheckboxArea(ComponentBase):
    _checkbox = 'xpath=.//*[contains(@data-crlat, "checkbox.")]'

    @property
    def checkbox(self):
        return ButtonBase(selector=self._checkbox, context=self._we)

    @property
    def non_runner(self):
        return self._get_webelement_text(selector=self._checkbox)

    def click(self):
        if self.non_runner:
            # i don't know if such verification is needed, just let it be here for now - mykhailo.s
            raise VoltronException('Cannot click as current runner is Non Runner')
        if not self.is_enabled():
            raise SiteServeException('Cannot click as Pool checkbox is not enabled')
        self.checkbox.click()

    def is_selected(self, expected_result=True, timeout=2, poll_interval=0.5, name=None):
        return wait_for_result(lambda: 'checked' in self.get_attribute('class'),
                               timeout=timeout,
                               name=f'Checkbox "{self.__class__.__name__}" selected status to be "{expected_result}"',
                               expected_result=expected_result)


class MultipleUKToteOutcome(Outcome):
    _select_check_box = 'xpath=.//*[@data-crlat="checkBox"]'

    def select(self):
        # can't implement it as CheckBoxBase because this element behaviour does not fit this class
        check_box = ButtonBase(selector=self._select_check_box, context=self._we)
        if check_box.is_enabled():
            check_box.click()
        else:
            raise VoltronException('Can\'t select UK Tote Pool checkbox as it is disabled')

    @property
    def checkbox(self):
        return ButtonBase(selector=self._select_check_box, context=self._we)


class SingleUKToteOutcome(Outcome):
    _item = 'xpath=.//*[@data-crlat="checkbox.area"]'
    _list_item_type = CheckboxArea
    _fixture_header_item = 'xpath=./../../..//*[@data-crlat="title"]'

    @property
    def items_as_ordered_dict(self) -> OrderedDict:
        items_we = self._find_elements_by_selector(selector=self._item, context=self._we)
        market_titles = self._find_elements_by_selector(selector=self._fixture_header_item, context=self._we)
        self._logger.debug(f'*** Found {len(items_we)} {self.__class__.__name__} - {self._list_item_type.__name__} items')
        items_ordered_dict = OrderedDict(
            [
                ('%s' % self._get_webelement_text(we=market_titles[items_we.index(item_we)]),
                 self._list_item_type(web_element=item_we)) for item_we in items_we
            ]
        )
        return items_ordered_dict


class SingleEventTotePoolType(RacingMarketSection):
    """ Win/Place, Exacta, Trifecta bets"""
    _list_item_type = SingleUKToteOutcome


class MultipleEventsTotePoolType(SingleEventTotePoolType):
    """ Placepot, Quadpot, Jackpot and Scoop6 bets """
    _item = 'xpath=.//*[@data-crlat="outcomeEntity" or @data-crlat="raceCard.odds"]'
    _list_item_type = MultipleUKToteOutcome
    _grouping_selection_buttons = 'xpath=.//*[@data-crlat="switchers"]'
    _grouping_selection_buttons_type = GroupingSelectionButtons
    _race_title = 'xpath=.//*[@data-crlat="raceTitle"]'

    @property
    def race_title(self):
        return self._get_webelement_text(selector=self._race_title, timeout=1)

    @property
    def grouping_buttons(self):
        return self._grouping_selection_buttons_type(selector=self._grouping_selection_buttons, context=self._we, timeout=5)


class UKToteSection(BaseContent):
    _url_pattern = r'^http[s]?:\/\/.+\/(horse-racing)\/[\w-]+\/[\w-]+\/[\w-]+\/[0-9]+\/[\w-]+\/[\w-]+$'
    _grouping_selection_buttons = 'xpath=.//*[@data-crlat="switchers"]'
    _grouping_selection_buttons_type = GroupingSelectionButtons
    _multiple_events_tote = 'xpath=.//*[@data-crlat="multipleEventsUKToteBet"]'
    _multiple_events_tote_pool_type = MultipleEventsTotePoolType
    _single_event_tote_pool_type = SingleEventTotePoolType
    _tote_pool_type = 'xpath=.//*[@data-crlat="UKTote.pool"]'
    _bet_builder = 'xpath=.//*[@data-crlat="betBuilder"]'
    _bet_builder_type = UKToteBetBuilder
    _fade_out_overlay = True
    _verify_spinner = True

    @property
    def grouping_buttons(self):
        return self._grouping_selection_buttons_type(self._grouping_selection_buttons, context=self._we)

    @property
    def pool(self):
        if self._find_element_by_selector(selector=self._multiple_events_tote, timeout=0) is not None:
            return MultipleEventsTotePoolType(selector=self._tote_pool_type, context=self._we, timeout=5)
        return SingleEventTotePoolType(selector=self._tote_pool_type, context=self._we, timeout=5)

    @property
    def bet_builder(self):
        return self._bet_builder_type(selector=self._bet_builder, context=self._we, timeout=1)

    @property
    def is_bet_builder_expanded(self, timeout=5, expected_result=True):
        section = self._find_element_by_selector(selector=self._bet_builder, context=self._we, timeout=2)
        if section:
            result = wait_for_result(lambda: 'expanded' not in section.get_attribute('class'),
                                     name=f'Bet builder expand status to be "{expected_result}"',
                                     expected_result=expected_result,
                                     timeout=timeout)
            self._logger.debug(f'*** Bet builder expanded status is {result}')
            return result
        return False
