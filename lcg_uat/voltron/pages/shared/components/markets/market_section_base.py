from selenium.common.exceptions import StaleElementReferenceException

from voltron.pages.shared.components.accordions_container import Accordion
from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.grouping_buttons import GroupingSelectionButtons
from voltron.pages.shared.components.primitives.buttons import ButtonBase, DefaultBetButton
from voltron.pages.shared.contents.base_contents.common_base_components.promotion_icons import PromotionIcons
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.waiters import wait_for_result


class MarketSectionHeader(ComponentBase):
    _title = 'xpath=.//*[@data-crlat="headerTitle.leftMessage"]'
    _cash_out_mark = 'xpath=.//*[@data-crlat="labelCashout"]'
    _span_count = 'xpath=./span'

    def _span_children_count(self):
        return len(self._find_elements_by_selector(selector=self._span_count, timeout=0))

    @property
    def title_text(self):
        if self._span_children_count() == 2:
            we = self._find_element_by_selector(self._title, context=self._we)
            if we is not None:
                return we.text
            else:
                raise VoltronException('No element matching %s was found' % self._title)
        elif self._span_children_count() == 1:
            we = self._find_element_by_selector(selector=self._span_count, timeout=0)
            if we is not None:
                return we.text
            else:
                raise VoltronException('No element matching %s was found' % self._span_count)
        else:
            return self._we.text

    def has_cash_out_mark(self, timeout=1, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._cash_out_mark,
                                                   timeout=0) is not None,
            name=f'Cash out mark status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)

    # TODO: vol_2421
    @property
    def cash_out_mark(self):
        return ComponentBase(self._cash_out_mark, timeout=1)


class MarketSection(Accordion):
    _market_section_header = 'xpath=.//*[@data-crlat="containerHeader"]'
    _market_section_header_type = MarketSectionHeader
    _market_list_item = 'xpath=.//*[@data-crlat="containerContent"]'
    _promotion_icons = 'xpath=.//*[@data-crlat="promotionIcons"]'
    _add_to_betslip_btn = 'xpath=.//*[contains(@data-crlat, "betButton")]'
    _show_all_button = 'xpath=.//*[text()="Show All"]'
    _show_less_button = 'xpath=.//*[text()="Show Less"]'

    @property
    def add_to_betslip_button(self):
        return DefaultBetButton(selector=self._add_to_betslip_btn, context=self._we)

    @property
    def show_all_button(self):
        return ButtonBase(selector=self._show_all_button, context=self._we, timeout=2)

    @property
    def has_show_all_button(self):
        show_all = self._find_element_by_selector(selector=self._show_all_button, timeout=2)
        return show_all.is_displayed() if show_all else False

    @property
    def show_less_button(self):
        return ButtonBase(selector=self._show_less_button, context=self._we, timeout=2)

    def has_show_less_button(self, timeout=2, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._show_less_button,
                                                   timeout=0) is not None,
            name=f'Show less btn to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)

    @property
    def market_section_header(self):
        return self._market_section_header_type(self._market_section_header, context=self._we)

    @property
    def name(self):
        return self.market_section_header.title_text

    def is_expanded(self, timeout=10, expected_result=True, bypass_exceptions=(StaleElementReferenceException, )):
        result = wait_for_result(lambda: 'is-expanded' in self.get_attribute('class'),
                                 name=f'"{self.__class__.__name__}" Accordion to expand',
                                 expected_result=expected_result,
                                 bypass_exceptions=bypass_exceptions,
                                 timeout=timeout)
        result = result if result else False
        self._logger.debug(f'*** "{self.__class__.__name__}" Accordion expanded status is "{result}"')
        return result

    def expand(self):
        if self.is_expanded(timeout=1):
            self._logger.warning(f'*** Bypassing accordion expand, since "{self.market_section_header.title_text}" already expanded')

        else:
            self._logger.debug(f'*** Expanding "{self.market_section_header.title_text}"')

            self.market_section_header.click()
            wait_for_result(lambda: self.is_expanded(), name='Expanded status', timeout=5)

    def collapse(self):
        if not self.is_expanded(timeout=1):
            self._logger.warning(f'*** Bypassing accordion collapse, since "{self.market_section_header.title_text}" already collapsed')
        else:
            self._logger.debug(f'*** Collapsing "{self.market_section_header.title_text}"')
            self.market_section_header.click()
            wait_for_result(lambda: self.is_expanded(), expected_result=False, name='Expanded status', timeout=5)

    @property
    def promotion_icons(self):
        return PromotionIcons(selector=self._promotion_icons, context=self._we)


class SwitcherMarketSection(MarketSection):
    _grouping_selection_buttons = 'xpath=.//*[@data-crlat="switchers"]'
    _grouping_selection_buttons_type = GroupingSelectionButtons

    @property
    def has_grouping_buttons(self):
        return self._find_elements_by_selector(self._grouping_selection_buttons, timeout=5) != []

    @property
    def grouping_buttons(self):
        if self.has_grouping_buttons:
            self._wait_active()
            return self._grouping_selection_buttons_type(self._grouping_selection_buttons, timeout=1, context=self._we)
        else:
            raise VoltronException('No Grouping Buttons object found')
