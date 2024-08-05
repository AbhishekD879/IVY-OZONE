from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.pages.shared.contents.base_contents.common_base_components.accordions_list import AccordionsList
from voltron.pages.shared.contents.base_contents.common_base_components.bet_button import BetButton
from voltron.pages.shared.contents.base_contents.common_base_components.tab_content import TabContent
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.waiters import wait_for_result


class PopularBetCard(ComponentBase):
    _name = 'xpath=.//*[@data-crlat="card-title-lable"]'
    _market_name = 'xpath=.//*[@data-crlat="card-team"]'
    _backed_text = 'xpath=.//*[@data-crlat="card-backed"]'
    _bet_button = 'xpath=.//*[@data-crlat="betButton"]'
    _position = 'xpath=.//*[@class="index"]'

    @property
    def position_number(self):
        return self._find_element_by_selector(selector=self._position, context=self._we)

    @property
    def bet_button(self):
        return BetButton(selector=self._bet_button, context=self._we)

    @property
    def name(self):
        return self._get_webelement_text(selector=self._name, context=self._we)

    @property
    def market_name(self):
        return self._get_webelement_text(selector=self._market_name, context=self._we)

    def has_backed_text(self, timeout=3, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._backed_text, timeout=3) is not None,
            timeout=timeout,
            expected_result=expected_result,
            name=f'"{self.__class__.__name__}" last updated to be {expected_result}')

    @property
    def backed_text(self):
        return self._get_webelement_text(selector=self._backed_text, context=self._we)


class PopularBetsAccordionsList(AccordionsList):
    _item = 'xpath=.//*[@data-crlat="card-main-popular" or @data-crlat="betEvent"]'
    _betslip_bar = 'xpath=.//*[@data-crlat="betslip-bar"]'
    _list_item_type = PopularBetCard
    _show_more = 'xpath=.//*[@data-crlat="toggleIcon"]'
    _add_to_betslip_btn = 'xpath=.//*[@data-crlat="add-to-betslip"]'
    _remove_from_betslip = 'xpath=.//*[@data-crlat="remove-from-betslip"]'
    _payout_desc = 'xpath=.//*[@data-crlat="stake-amt"]'
    _scroll_container = 'xpath=.//*[@data-crlat="scroll-container"]'
    _description_text = 'xpath=.//*[@data-crlat="top-five-desc"]'

    def has_add_to_betslip_bar(self, timeout=3, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._betslip_bar, timeout=3) is not None,
            timeout=timeout,
            expected_result=expected_result,
            # it is a description string used for logging purposes, indicating the class name and the expected result.
            name=f'"{self.__class__.__name__}" last updated to be {expected_result}')

    @property
    def add_to_betslip_button(self):
        return ButtonBase(selector=self._add_to_betslip_btn, context=self._we)

    @property
    def remove_from_betslip(self):
        return ButtonBase(selector=self._remove_from_betslip, context=self._we)

    @property
    def scroll_container(self):
        return ButtonBase(selector=self._scroll_container, context=self._we)

    def has_show_more_less(self, expected_result=True, timeout=2):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._show_more, context=self._we,
                                                                      timeout=0) is not None,
                               name=f'Show More button display status to be {expected_result}',
                               expected_result=expected_result, timeout=timeout)

    @property
    def toggle_icon_name(self):
        return self._get_webelement_text(self._show_more, timeout=0, context=self._we)

    @property
    def show_more_less(self):
        return ButtonBase(selector=self._show_more, context=self._we)

    @property
    def payout_desc(self):
        return self._get_webelement_text(selector=self._payout_desc, context=self._we)

    @property
    def description_text(self):
        return self._get_webelement_text(we=self._description_text)


class TimeFilterItem(ComponentBase):
    @property
    def name(self):
        return self._get_webelement_text(we=self._we)


class TimeFilters(ComponentBase):
    _item = 'xpath=.//*[@data-crlat="item"]'
    _list_item_type = TimeFilterItem
    _current = 'xpath=.//*[@data-crlat="item"]//*[contains(@class,"active")]'

    @property
    def current(self) -> str:
        return self._get_webelement_text(selector=self._current, context=self._we)


class BackedFilterItem(ComponentBase):
    @property
    def name(self):
        return self._get_webelement_text(we=self._we)


class BackedFiltersDropDown(ComponentBase):
    _item = 'xpath=.//*[@data-crlat="mostBacked-item"]'
    _list_item_type = BackedFilterItem

    def select_item_with_name(self, item_name=""):
        selector_for_item_name = self._item.replace(']', f' and text()="{item_name}"]')
        we = wait_for_result(lambda: BackedFilterItem(selector=selector_for_item_name, context=self._we),
                             bypass_exceptions=(
                             NoSuchElementException, StaleElementReferenceException, VoltronException))
        if not we:
            raise VoltronException(f'Backed Filter is not found with the name of {item_name}')
        we.click()


class BackedFilters(ComponentBase):
    _backed_sort_filter = 'xpath=.//*[@data-crlat="sort-filter"]'
    _backed_filter_chevron_up = 'xpath=.//*[@data-crlat="chevron-icon-up"]'
    _backed_filter_chevron_down = 'xpath=.//*[@data-crlat="chevron-icon-down"]'
    _backed_dropdown = 'xpath=.//*[@data-crlat="mostBacked"]'
    _backed_time_filter = 'xpath=.//*[@data-crlat="mostBacked-item"]'

    @property
    def backed_sort_filter(self):
        return ButtonBase(selector=self._backed_sort_filter, context=self._we)

    @property
    def backed_time_filter(self):
        return ButtonBase(selector=self._backed_time_filter, context=self._we)

    @property
    def backed_dropdown(self):
        return BackedFiltersDropDown(selector=self._backed_dropdown, timeout=3)

    @property
    def backed_filter_chevron_up(self):
        return self._find_element_by_selector(selector=self._backed_filter_chevron_up, timeout=1)

    @property
    def backed_filter_chevron_down(self):
        return self._find_element_by_selector(selector=self._backed_filter_chevron_down, timeout=1)

    def has_backed_filter_chevron_down(self):
        return self._find_element_by_selector(selector=self._backed_filter_chevron_down, timeout=1)


class DescriptionContainer(ComponentBase):
    _description = 'xpath=.//*[@data-crlat="description-value"]'
    _description_close = 'xpath=.//*[@data-crlat="description-close-icon"]'
    _description_info_icon = 'xpath=.//*[@data-crlat="description-info-icon"]'

    @property
    def description(self):
        return self._get_webelement_text(selector=self._description)

    @property
    def close(self):
        return ButtonBase(selector=self._description_close)

    def has_info_icon(self, timeout=2, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._description_info_icon, timeout=0) is not None,
            timeout=timeout,
            expected_result=expected_result,
            name=f'"{self.__class__.__name__}" description icon status to be {expected_result}')


class PopularBetsTabContent(TabContent):
    _description_container = 'xpath=.//*[@data-crlat="blurb-market-description"]'
    _type_of_description = DescriptionContainer
    _accordian_header = 'xpath=.//*[@data-crlat="containerHeader"]'
    _accordions_list = 'xpath=.//*[@data-crlat="popular-cards-list" or @data-crlat="for-you-cards-list"]'
    _backed_filter = 'xpath=.//*[@data-crlat="backed-text"]'
    _no_bets_message = 'xpath=.//*[@class="no-bets-message"]'
    _time_filters = 'xpath=.//*[@data-crlat="filter"]'
    _last_updated = 'xpath=.//*[@data-crlat="lastUpdated"]'
    _accordions_list_type = PopularBetsAccordionsList
    _login_button = 'xpath=.//*[@data-crlat="signInButton"]'
    _no_foryou_bet_description = 'xpath=.//*[@ data-crlat="noBetsDesc"]'
    _go_to_football = 'xpath=.//*[@data-crlat="noBettingCta"]'
    _displayname_in_foryou = 'xpath=.//*[@data-crlat="displayName"]'

    @property
    def accordian_header(self):
        return self._get_webelement_text(selector=self._accordian_header, context=self._we)

    @property
    def displayname_in_foryou(self):
        return self._get_webelement_text(selector=self._displayname_in_foryou, context=self._we)

    def has_no_bets_message(self, timeout=3, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._no_bets_message, timeout=3) is not None,
            timeout=timeout,
            expected_result=expected_result,
            name=f'"{self.__class__.__name__}" last updated to be {expected_result}')

    def has_last_updated(self, timeout=3, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._last_updated, timeout=3) is not None,
            timeout=timeout,
            expected_result=expected_result,
            name=f'"{self.__class__.__name__}" last updated to be {expected_result}')

    @property
    def last_updated(self):
        return self._get_webelement_text(selector=self._last_updated)

    def has_time_filters(self, timeout=3, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._time_filters, timeout=2) is not None,
            timeout=timeout,
            expected_result=expected_result,
            name=f'"{self.__class__.__name__}" time filter to be {expected_result}')

    @property
    def backed_filter(self):
        return BackedFilters(selector=self._backed_filter, timeout=2)

    def has_backed_filter(self, timeout=3, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._backed_filter, timeout=2) is not None,
            timeout=timeout,
            expected_result=expected_result,
            name=f'"{self.__class__.__name__}" backed status to be {expected_result}')

    @property
    def timeline_filters(self):
        return TimeFilters(selector=self._time_filters, timeout=5)

    def has_description_container(self, timeout=2, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._description_container, timeout=0) is not None,
            timeout=timeout,
            expected_result=expected_result,
            name=f'"{self.__class__.__name__}" YourCall icon status to be {expected_result}')

    @property
    def description_container(self):
        return self._type_of_description(selector=self._description_container)

    @property
    def login_button(self):
        return ButtonBase(selector=self._login_button, context=self._we)

    def has_login_button(self, timeout=3, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._login_button, timeout=3) is not None,
            timeout=timeout,
            expected_result=expected_result,
            name=f'"{self.__class__.__name__}" last updated to be {expected_result}')

    def has_no_foryou_bet_description(self, timeout=2, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._no_foryou_bet_description, timeout=0) is not None,
            timeout=timeout,
            expected_result=expected_result,
            name=f'"{self.__class__.__name__}" YourCall icon status to be {expected_result}')

    @property
    def no_foryou_bet_description(self):
        return self._get_webelement_text(selector=self._no_foryou_bet_description, context=self._we)

    @property
    def go_to_football(self):
        return ButtonBase(selector=self._go_to_football, context=self._we)

    def has_go_to_football(self, timeout=3, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._go_to_football, timeout=3) is not None,
            timeout=timeout,
            expected_result=expected_result,
            name=f'"{self.__class__.__name__}" last updated to be {expected_result}')
