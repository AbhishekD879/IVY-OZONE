import re

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.keys import Keys

from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.pages.shared.components.primitives.buttons import SpinnerButtonBase
from voltron.pages.shared.components.primitives.checkboxes import CheckBoxBase
from voltron.pages.shared.components.primitives.inputs import InputBase
from voltron.pages.shared.components.primitives.stake import Stake
from voltron.pages.shared.contents.base_contents.racing_base_components.meeting_selector import MeetingSelector
from voltron.pages.shared.contents.bet_receipt.tote_bet_receipt import ToteBetReceiptSectionsList
from voltron.pages.shared.contents.edp.racing_edp_market_section import Outcome
from voltron.pages.shared.contents.edp.racing_edp_market_section import RacingMarketSection
from voltron.pages.shared.contents.edp.racing_event_details import EventMarketsList
from voltron.pages.shared.contents.edp.racing_event_details import RacingEDPTabContent
from voltron.pages.shared.contents.edp.racing_event_details import RacingEventDetails
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.js_functions import get_value
from voltron.utils.waiters import wait_for_result


class ToteEventHeader(ComponentBase):
    _event_time = 'xpath=.//*[@data-crlat="eventName"]'
    _distance = 'xpath=.//*[@data-crlat="eventDistance"]'

    @property
    def event_time(self):
        text = self._get_webelement_text(selector=self._event_time)
        find = re.search(r'([\d:]+)[\w\s.-]+', text)
        return find.group(1) if find else ''

    @property
    def distance(self):
        return self._get_webelement_text(selector=self._distance)


class ExactaTrifectaSection(ComponentBase):
    _first = 'xpath=(.//*[@data-crlat="exPool.placeCheckBox"])[1]'
    _second = 'xpath=(.//*[@data-crlat="exPool.placeCheckBox"])[2]'
    _third = 'xpath=(.//*[@data-crlat="exPool.placeCheckBox"])[3]'

    @property
    def has_first(self):
        return self._find_element_by_selector(selector=self._first, timeout=0) is not None

    @property
    def has_second(self):
        return self._find_element_by_selector(selector=self._second, timeout=0) is not None

    @property
    def has_third(self):
        return self._find_element_by_selector(selector=self._third, timeout=0) is not None

    @property
    def first(self):
        return CheckBoxBase(selector=self._first, context=self._we)

    @property
    def second(self):
        return CheckBoxBase(selector=self._second, context=self._we)

    @property
    def third(self):
        return CheckBoxBase(selector=self._third, context=self._we)


class ToteInputBase(InputBase):

    @property
    def value(self):
        self.scroll_to_we()
        return get_value(self._we)

    @value.setter
    def value(self, value):
        self.scroll_to_we()
        self._we.clear()
        self._we.send_keys(str(value))
        self._we.send_keys(Keys.SHIFT + Keys.TAB)
        self._we.click()
        self._we.send_keys(Keys.SHIFT + Keys.TAB)

    @property
    def is_empty(self):
        return 'ng-not-empty' not in self.get_attribute('class')


class ToteOutcome(Outcome):
    _expand_plus_icon = 'xpath=.//*[@data-crlat="toggleIcon"]'
    _collapse_minus_icon = 'xpath=.//*[@data-crlat="minusIcon"]'
    _currency = 'xpath=.//*[@data-crlat="pool.currencySymbol"]'
    _input_number = 'xpath=.//*[@data-crlat="stakeInput"]'
    _error_msg = 'xpath=.//*[@data-crlat="pool.outcomeError"]'
    _exacta_trifecta_section = 'xpath=.//*[@data-crlat="exPool.checkboxesForm"]'
    _guide = 'xpath=.//*[@data-crlat="guide"]'

    @property
    def exacta_trifecta_section(self):
        return ExactaTrifectaSection(selector=self._exacta_trifecta_section, context=self._we)

    @property
    def guide(self):
        return self._get_webelement_text(selector=self._guide, timeout=2)

    def has_expand_plus_icon(self, timeout=2, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._expand_plus_icon,
                                                   timeout=0) is not None,
            name=f'Expand Plus Icon status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)

    @property
    def expand_plus_icon(self):
        return ButtonBase(selector=self._expand_plus_icon, context=self._we)

    @property
    def collapse_minus_icon(self):
        return ButtonBase(selector=self._collapse_minus_icon, context=self._we)

    def is_expanded(self, timeout=0.3, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._expanded_summary,
                                                   context=self._we,
                                                   timeout=0) is not None,
            name=f'Expanded summary status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)

    def expand(self):
        self.scroll_to_we()
        if self.is_expanded():
            self._logger.warning(f'*** Bypassing accordion expand, since "{self.horse_name}" already expanded')
        else:
            self._logger.debug(f'*** Expanding "{self.horse_name}"')
            self.expand_plus_icon.click()
            wait_for_result(lambda: self.is_expanded(), name='Expanded status', timeout=5)

    def collapse(self):
        self.scroll_to_we()
        if not self.is_expanded():
            self._logger.debug(f'*** Bypassing accordion collapse, since "{self.horse_name}" already collapsed')
        else:
            self._logger.debug(f'*** Collapsing "{self.horse_name}"')
            self.collapse_minus_icon.click()
            wait_for_result(lambda: self.is_expanded(), expected_result=False, name='Expanded status', timeout=5)

    def get_currency_symbol(self):
        return self._get_webelement_text(selector=self._currency, context=self._we)

    @property
    def stake(self):
        return ToteInputBase(selector=self._input_number, context=self._we)

    def enter_stake(self, value):
        if not isinstance(value, str):
            value = str(value)
        self.stake.scroll_to()
        self.stake.value = value
        wait_for_result(lambda: self.stake.is_empty,
                        expected_result=False,
                        name='Stake input field not empty',
                        timeout=1)

    def wait_for_error_msg(self, expected_result=True, timeout=2):
        result = wait_for_result(lambda: self._get_webelement_text(selector=self._error_msg),
                                 name='Outcome error message to show up/disappear',
                                 expected_result=expected_result,
                                 timeout=timeout,
                                 bypass_exceptions=(NoSuchElementException,
                                                    StaleElementReferenceException,
                                                    VoltronException))
        if bool(result) is expected_result:
            return result
        return ''

    @property
    def error_msg(self):
        return self._get_webelement_text(selector=self._error_msg, context=self._we, timeout=2)


class ToteTotalStake(Stake):
    _value = 'xpath=.//*[@data-crlat="totalStake"]'
    _converted_value = 'xpath=.//*[@data-crlat="convertedTotalStake"]'

    @property
    def converted_value(self):
        return self._get_webelement_text(selector=self._converted_value, context=self._we)

    @property
    def converted_currency(self):
        value = self.converted_value
        currency = re.match(r'^([^0-9]+)', value)
        if currency:
            return currency.group(1)
        else:
            raise VoltronException('Error occurred parsing stake string "%s"' % value)

    @property
    def converted_amount(self):
        value = self.converted_value
        if value:
            amount = re.match(r'^([^0-9]+)([0-9]+[\,|\.][0-9]{2})', value)
            if amount:
                return amount.group(2)
            else:
                raise VoltronException('Error occurred parsing stake string "%s"' % value)
        return ''

    @property
    def amount(self):
        we = self._find_element_by_selector(selector=self._value)
        self.scroll_to_we(web_element=we)
        value = self._get_webelement_text(we=we)
        return self.strip_currency_sign(value)


class ToteBetNowSection(ComponentBase):
    _pool_stake = 'xpath=.//*[@data-crlat="poolStakeInput"]'
    _total_stake = 'xpath=.//*[@data-crlat="totalStakeContainer"]'
    _bet_now_button = 'xpath=.//*[@data-crlat="placeBetsButton"]'
    _clear_betslip_button = 'xpath=.//*[@data-crlat="clearBetsButton"]'
    _error_msg = 'xpath=.//*[@data-crlat="pool.totalStakeError"]'

    @property
    def has_pool_stake(self):
        return self._find_element_by_selector(selector=self._pool_stake, timeout=0) is not None

    @property
    def pool_stake(self):
        return InputBase(selector=self._pool_stake, context=self._we)

    def enter_stake(self, value):
        if not isinstance(value, str):
            value = str(value)
        self.pool_stake.value = value

    @property
    def total_stake(self):
        return ToteTotalStake(selector=self._total_stake, context=self._we)

    @property
    def bet_now_button(self):
        return SpinnerButtonBase(selector=self._bet_now_button, context=self._we)

    @property
    def clear_betslip_button(self):
        return ButtonBase(selector=self._clear_betslip_button, context=self._we)

    @property
    def has_error_msg(self):
        return self._find_element_by_selector(selector=self._error_msg, timeout=0.1) is not None

    @property
    def error_msg(self):
        return self._get_webelement_text(selector=self._error_msg, context=self._we, timeout=3)


class ToteMarketSection(RacingMarketSection):
    _item = 'xpath=.//*[@data-crlat="raceCard.outcome"]'
    _list_item_type = ToteOutcome


class ToteEventMarketsList(EventMarketsList):
    _item = 'xpath=.//*[contains(@data-crlat, "marketOutcomes")]'
    _list_item_type = ToteMarketSection
    _betslip_bet_container = ToteBetNowSection
    _betslip_bet = 'xpath=.//*[@data-crlat="pool.betContainer"]'
    _error = 'xpath=.//*[@data-crlat="pool.eventError"]'
    _event_header = 'xpath=.//*[@data-crlat="eventNameContainer"]'
    _event_header_type = ToteEventHeader
    _market_tabs_list = 'xpath=.//*[@data-crlat="switchers"]'

    @property
    def event_header(self):
        return self._event_header_type(self._event_header, context=self._we)

    @property
    def betslip_bet_container(self):
        return self._betslip_bet_container(selector=self._betslip_bet, context=self._we)

    @property
    def event_error(self):
        we = self._find_element_by_selector(selector=self._error, timeout=2)
        if we:
            self.scroll_to_we(web_element=we)
            err = self._get_webelement_text(we=we)
            wait_for_result(lambda: err != self._get_webelement_text(selector=self._error),
                            name='Waiting for error message to change',
                            timeout=2)
            return self._get_webelement_text(selector=self._error)
        return ''


class ToteEDPTabContent(RacingEDPTabContent):
    _event_markets_list_type = ToteEventMarketsList
    _bet_description = 'xpath=.//*[@data-crlat="pool.betDescription"]'
    _pool_size_value = 'xpath=.//*[@data-crlat="poolSize"]'
    _pool_size_label = 'xpath=.//*[@data-crlat="label.poolSize"]'
    _meeting_selector = 'xpath=.//*[@data-crlat="meetingNavigator"]'
    _meeting_selector_type = MeetingSelector
    _bet_receipt_sections_list = 'xpath=.//*[@data-crlat="pool.betReceiptData"]'
    _bet_receipt_list_type = ToteBetReceiptSectionsList

    def _wait_active(self, timeout=0):
        """
        Bypassing wait active
        """
        pass

    @property
    def bet_description(self):
        return self._get_webelement_text(selector=self._bet_description, timeout=2)

    @property
    def _pool_size(self):
        text = self._get_webelement_text(selector=self._pool_size_value, timeout=2)
        return re.findall(r'([\d.,]+)', text)

    @property
    def user_currency_pool_size(self):
        return self._pool_size[0] if len(self._pool_size) >= 1 else ''

    @property
    def pool_currency_pool_size(self):
        return self._pool_size[1] if len(self._pool_size) >= 2 else ''

    @property
    def pool_size_label(self):
        return self._get_webelement_text(selector=self._pool_size_label, timeout=5)

    @property
    def meeting_selector(self):
        return self._meeting_selector_type(selector=self._meeting_selector, context=self._we)

    @property
    def bet_receipt_section_list(self):
        return self._bet_receipt_list_type(selector=self._bet_receipt_sections_list, context=self._we)


class ToteEventDetails(RacingEventDetails):
    _url_pattern = r'^http[s]?:\/\/.+\/(tote)\/event\/[0-9]+'
    _tab_content_type = ToteEDPTabContent
