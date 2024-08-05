import re
from collections import OrderedDict

from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import WebDriverException

from voltron.pages.shared.components.accordions_container import Accordion
from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.markets.build_your_bet.byb_player_bets_market import BYBPlayerBetsMarket
from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.pages.shared.components.primitives.buttons import IconBase
from voltron.pages.shared.components.primitives.text_labels import TextBase
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.waiters import wait_for_result


class SummaryCounter(ComponentBase):
    _dashboard_icon = 'xpath=.//*[@data-crlat="icon.dashboard"]'
    _counter = 'xpath=.//*[@data-crlat="selection.counter"]'

    @property
    def icon(self):
        return IconBase(selector=self._dashboard_icon, context=self._we, timeout=2)

    @property
    def value(self):
        value = self._get_webelement_text(selector=self._counter)
        return value if value else '0'


class SummaryDescription(ComponentBase):
    _dashboard_default_title = 'xpath=.//*[@data-crlat="yourcall.dashboardTitle"]'
    _dashboard_market_text = 'xpath=.//*[@data-crlat="yourcall.dashboardText"]'

    @property
    def dashboard_title(self):
        return self._get_webelement_text(selector=self._dashboard_default_title)

    @property
    def dashboard_market_text(self):
        return self._get_webelement_text(selector=self._dashboard_market_text)

    def is_element_truncated(self):
        return self.is_truncated(selector=self._dashboard_market_text)


class SummaryPlaceBet(ComponentBase):
    _value = 'xpath=.//*[@data-crlat="yourcall.odds"]'
    _text = 'xpath=.//*[@data-crlat="yourcall.placeBet"]'
    _fade_out_overlay = True
    _verify_spinner = True

    def has_price(self, expected_result=True, timeout=1):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._value, timeout=0) is not None,
                               expected_result=expected_result,
                               timeout=timeout,
                               name=f'Price status to be "{expected_result}"')

    @property
    def value(self):
        text = self._get_webelement_text(selector=self._value)
        matcher = re.search(r'^([\-0-9]+.[\-0-9]*)'+'|' + r'^([\-0-9]+/[\-0-9]*)',  text)
        if matcher is not None:
            return True
        else:
            raise VoltronException(f'Odds format is not correct "{text}"')

    @property
    def value_text(self):
        return self._get_webelement_text(selector=self._value, timeout=1)

    @property
    def text(self):
        return self._get_webelement_text(selector=self._text, timeout=1)

    def click(self, timeout=10):
        self.scroll_to_we()
        try:
            self.perform_click()
        except WebDriverException as e:
            raise VoltronException(f'Can not click on {self.__class__.__name__}. {e}')
        self._spinner_wait(timeout=timeout)


class OpenCloseButton(ButtonBase):
    _name = 'xpath=.//*[@data-crlat="yourcallOpenCloseText"]'
    _arrow = 'xpath=.//*[@data-crlat="icon.arrowdown"]'

    @property
    def name(self):
        return self._get_webelement_text(selector=self._name, timeout=0.5)

    def has_up_down_arrow(self, expected_result=True, timeout=1):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._arrow, timeout=0)
                               is not None,
                               expected_result=expected_result,
                               timeout=timeout,
                               name=f'Up Down Arrow status to be "{expected_result}"')


class BYBSummary(ComponentBase):
    _summary_counter = 'xpath=.//*[@data-crlat="counterBlock"]'
    _summary_counter_type = SummaryCounter
    _summary_description = 'xpath=.//*[@data-crlat="descriptionBlock"]'
    _summary_description_type = SummaryDescription
    _place_bet = 'xpath=.//*[@data-crlat="oddBlock"]'
    _place_bet_type = SummaryPlaceBet
    _open_close_btn = 'xpath=.//*[@data-crlat="open.closeButton"]'

    @property
    def summary_counter(self):
        return SummaryCounter(selector=self._summary_counter)

    @property
    def summary_description(self):
        return SummaryDescription(selector=self._summary_description)

    @property
    def place_bet(self):
        context = SummaryPlaceBet(selector=self._place_bet, context=self._we, timeout=2)
        context.is_enabled(timeout=0.5)
        return context

    def has_place_bet_button(self, expected_result=True, timeout=1):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._place_bet, context=self._we, timeout=0) is not None,
                               expected_result=expected_result,
                               timeout=timeout,
                               name=f'Place bet Button status to be "{expected_result}"')

    @property
    def open_close_toggle_button(self):
        return OpenCloseButton(selector=self._open_close_btn, context=self._we)

    def wait_for_counter_change(self, initial_counter, timeout=5):
        return wait_for_result(lambda: self.summary_counter.value != initial_counter,
                               name='Counter to change',
                               timeout=timeout
                               )


class BYBListItem(ComponentBase):
    _market_text = 'xpath=.//*[@data-crlat="marketTitle"]'
    _selection_text = 'xpath=.//*[@data-crlat="selectionTitle"]'
    _remove_btn = 'xpath=.//*[@data-crlat="removeSelectionButton"]'
    _edit_btn = 'xpath=.//*[@data-crlat="marketEditButton"]'
    _error_icon = 'xpath=.//*[@data-crlat="selection.error"]'

    @property
    def market_text(self):
        self.scroll_to()
        return self._get_webelement_text(selector=self._market_text, timeout=1.5)

    @property
    def selection_text(self):
        self.scroll_to()
        return self._get_webelement_text(selector=self._selection_text, timeout=1.5)

    @property
    def name(self):
        name = self.market_text + ' ' + self.selection_text
        return name.strip()

    @property
    def edit_button(self):
        return ButtonBase(selector=self._edit_btn, context=self._we)

    def has_remove_button(self, expected_result=True, timeout=1):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._remove_btn,
                                                                      timeout=0.5) is not None,
                               expected_result=expected_result,
                               timeout=timeout,
                               name=f'Remove Button status to be "{expected_result}"')

    @property
    def remove_button(self):
        return ButtonBase(selector=self._remove_btn, context=self._we)


class OutcomeEditHeader(ComponentBase):
    _header_title = 'xpath=.//*[@data-crlat="edit.section.text"]'
    _done_button = 'xpath=.//*[@data-crlat="doneButton"]'

    def _wait_active(self, timeout=0):
        try:
            self._we = self._find_myself()
        except StaleElementReferenceException:
            self._logger.debug(f'*** Overriding StaleElementReferenceException in {self.__class__.__name__} - {__name__}')
            self._we = self._find_myself()

    @property
    def title(self):
        return self._get_webelement_text(selector=self._header_title, timeout=1)

    @property
    def done_button_text(self):
        return self._get_webelement_text(selector=self._done_button, timeout=1)

    @property
    def done_button(self):
        # TODO fix timing issue VOL-1160
        from time import sleep
        sleep(2)
        return ButtonBase(selector=self._done_button, context=self._we)


class OutcomeEdit(ComponentBase):
    _header = 'xpath=.//*[@data-crlat="dash.item"]'
    _header_type = OutcomeEditHeader
    _selection_edit = 'xpath=.//*[@data-crlat="playerBetsForm"]'

    @property
    def header(self):
        try:
            return OutcomeEditHeader(selector=self._header, context=self._we)
        except StaleElementReferenceException:
            self._logger.debug(f'*** Overriding StaleElementReferenceException in {self.__class__.__name__}')
            return OutcomeEditHeader(selector=self._header, context=self._we, timeout=5)

    # BYBPlayerBetsMarket suggested that have only one edit market - Player Bets
    @property
    def edit(self):
        try:
            return BYBPlayerBetsMarket(selector=self._selection_edit, context=self._we)
        except StaleElementReferenceException:
            self._logger.debug(f'*** Overriding StaleElementReferenceException in {self.__class__.__name__}')
            return BYBPlayerBetsMarket(selector=self._selection_edit, context=self._we, timeout=5)


class BYBDashboardItemsList(ComponentBase):
    _item = 'xpath=.//*[@data-crlat="selection.edit"]'
    _list_item_type = BYBListItem
    _edit_selection = 'xpath=.//*[@data-crlat="edit.section"]'
    _edit_selection_type = OutcomeEdit

    def _wait_active(self, timeout=10):
        self._we = self._find_myself()
        wait_for_result(lambda: all(self.items_as_ordered_dict),
                        name=f'{self.__class__.__name__} – {self._list_item_type.__name__} to load',
                        timeout=timeout)

    @property
    def edit_selection(self):
        return OutcomeEdit(selector=self._edit_selection, context=self._we)

    def has_edit(self, expected_result=True, timeout=5):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._edit_selection, context=self._we, timeout=0),
            name=f'Edit block available status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)

    @property
    def items_as_ordered_dict(self) -> OrderedDict:
        """
        Override because of duplicated selection name, so if we have duplicated name
        it'll add sequence number to item key, else it works as in CommonBase
        """
        items_we = self._find_elements_by_selector(selector=self._item, context=self._we)
        self._logger.debug(f'*** Found {len(items_we)} {self.__class__.__name__} – {self._list_item_type.__name__} items')
        items_ordered_dict = OrderedDict()
        for index, item_we in enumerate(items_we):
            value = self._list_item_type(web_element=item_we)
            key = value.name
            key = '%s-%s' % (index, key) if key in items_ordered_dict else key
            items_ordered_dict[key] = value
        return items_ordered_dict


class InfoPanel(ComponentBase):
    _icon_alert = 'xpath=.//*[@data-crlat="icon.alert"]'
    _text = 'xpath=.//*[@data-crlat="errorMessageText"]'
    _text_2 = 'xpath=.//*[@data-crlat="errorValidationError"]'

    @property
    def text(self):
        """
        Needed because of different error messages have different locators but both present in dom
        """
        text = self._get_webelement_text(selector=self._text, context=self._we, timeout=0.5)
        if text:
            return text
        else:
            return self._get_webelement_text(selector=self._text_2, context=self._we, timeout=0.5)


class BYBDashboardSection(Accordion):
    _info_panel = 'xpath=.//*[@data-crlat="infPan.msg"]'
    _info_panel_type = InfoPanel
    _summary = 'xpath=.//*[@data-crlat="yourcallSummary"]'
    _summary_type = BYBSummary
    _byb_selection_list = 'xpath=.//*[@data-crlat="containerContent"]'
    _byb_selection_list_type = BYBDashboardItemsList
    _price_not_available_message = 'xpath=.//*[@data-crlat="errorMessageText"]'

    @property
    def info_panel(self):
        return InfoPanel(selector=self._info_panel, context=self._we)

    def wait_for_info_panel(self, expected_result=True, timeout=1):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._info_panel, context=self._we,
                                                                      timeout=0) is not None,
                               name=f'Info panel displayed status to be "{expected_result}"',
                               expected_result=expected_result,
                               timeout=timeout)

    @property
    def byb_summary(self):
        return BYBSummary(selector=self._summary, context=self._we)

    @property
    def outcomes_section(self):
        return BYBDashboardItemsList(selector=self._byb_selection_list, context=self._we, timeout=3)

    def is_expanded(self, timeout=1, expected_result=True, bypass_exceptions=(StaleElementReferenceException, )):
        result = wait_for_result(lambda: 'expanded' in self.get_attribute('class'),
                                 name=f'"{self.__class__.__name__}" Dashboard expand status to be "{expected_result}"',
                                 expected_result=expected_result,
                                 timeout=timeout,
                                 bypass_exceptions=bypass_exceptions)
        self._logger.debug(f'"{self.__class__.__name__}" Dashboard expanded status is "{result}"')
        return result

    def has_price_not_available_message(self, timeout=1, expected_result=False):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._price_not_available_message,
                                                                      timeout=0) is not None,
                               name=f'Price not available message status to be "{expected_result}"',
                               expected_result=expected_result,
                               timeout=timeout)

    @property
    def price_not_available_message(self):
        return TextBase(selector=self._price_not_available_message, context=self._we, timeout=0)
