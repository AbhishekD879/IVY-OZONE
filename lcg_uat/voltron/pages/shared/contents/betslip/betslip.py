from selenium.common.exceptions import StaleElementReferenceException

import voltron.environments.constants as vec
from voltron.pages.shared.components.quick_bet_quick_deposit_panel import GVCQuickDeposit
from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.info_panel import InfoPanel
from voltron.pages.shared.components.odds_boost_header import OddsBoostHeader
from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.pages.shared.components.primitives.text_labels import TextBase
from voltron.pages.shared.contents.betslip.betslip_bet_now_section import BetNowSection
from voltron.pages.shared.contents.betslip.betslip_overask_trader_offer import OveraskTraderOfferSection
from voltron.pages.shared.contents.betslip.betslip_sections_list import BetSlipSectionHeader
from voltron.pages.shared.contents.betslip.betslip_sections_list import BetSlipSectionsList, LottoBetSlipSectionsList
from voltron.pages.shared.contents.betslip.betslip_user_header import UserHeader
from voltron.pages.shared.contents.betslip.overask import Overask
from voltron.pages.shared.contents.trending_bets.trending_bets import TrendingBets
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.js_functions import click
from voltron.utils.waiters import wait_for_result
from voltron.pages.shared.components.primitives.text_labels import LinkBase


class CloseButton(ButtonBase):

    def click(self, scroll_to=True):
        if scroll_to:
            self.scroll_to_we()
        self._logger.debug(
            f'*** User has clicked "{self._we.text}" button. Call "{self.__class__.__name__}.click" method'
        )
        click(self._we)


class BetSlip(ComponentBase):
    _betslip_sections_list = 'xpath=.//*[contains(@class,"bs-wrapper-block")]'
    _betslip_sections_list_type = BetSlipSectionsList
    _betnow_section = 'xpath=.//*[contains(@data-crlat,"bsFoot")]'
    _betnow_section_type = BetNowSection
    _no_selections_title = 'xpath=.//*[@data-crlat="noSelTitle"]'
    _no_selections_message = 'xpath=.//*[@data-crlat="noSelMsg"]'
    _start_betting_button = 'xpath=.//*[@data-crlat="startBetting"]'
    _betslip_error_message = 'xpath=.//*[@data-crlat="bs.ntfErr"]'
    _price_change_warning_message = 'xpath=.//*[@data-crlat="stake.errorMessage"]'
    _suspended_account_warning_message = 'xpath=.//*[contains(@class, "bottom warning")] | .//*[contains(@class, "footer-notifications")]/div'
    _incorrect_bet_amount_warning_message = 'xpath=.//*[@data-crlat="infPan.msg"]'
    _betslip_deposit = 'xpath=.//*[@data-crlat="QD"] | .//quick-deposit-iframe'
    _close_button = 'xpath=.//*[@data-crlat="sidebarClose"]'
    _page_title = 'xpath=.//*[@data-crlat="betslipHeader"] | .//*[@data-crlat="bsTab"]'
    _betslip_header = 'xpath=.//*[@data-crlat="sidebarMenuHeader"]'
    _hide_balance_option = 'xpath=.//*[@data-crlat="hideBalanceOption"]'
    _quick_deposit_option = 'xpath=.//*[@data-crlat="depositOption"]'
    _odds_boost_header = 'xpath=.//*[@data-crlat="oddsBoostBetslipHeader"]'
    _betslip_balance_button = 'xpath=.//*[@data-crlat="betslipBalanceButton"]'
    _odds_boost_header_type = OddsBoostHeader
    _remove_all_button = 'xpath=.//*[@data-crlat="removeAllSelections"]'
    _your_selection_header = 'xpath=.//*[@data-crlat="bsHead"]'
    _your_selection_header_type = BetSlipSectionHeader
    _overask_item = 'xpath=.//*[@data-crlat="oPage"]'
    _overask_type = Overask
    _overask_trader_section_type = OveraskTraderOfferSection
    _loading_screen = 'xpath=.//*[@data-crlat="bsLoad"]'
    _fade_out_overlay = True
    _verify_spinner = True
    _trending_bets_type = TrendingBets
    _trending_bets = 'xpath=.//*[@data-crlat="trending-acc"]'
    _max_payout_msg = 'xpath=.//*[@data-crlat="maxPayoutMsg"]'
    _max_payout_link = 'xpath=.//*[@data-crlat="maxPayOutLink"]'

    def has_trending_bet_carousel(self, expected_result=True, timeout=3):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._trending_bets, timeout=0) is not None,
            name=f'"trending bet carousel" shown status "{expected_result}"',
            timeout=timeout,
            expected_result=expected_result)

    @property
    def trending_bets_section(self):
        return self._trending_bets_type(selector=self._trending_bets, context=self._we)

    @property
    def header(self):
        return UserHeader(selector=self._betslip_header)

    @property
    def loading_screen(self):
        return ComponentBase(selector=self._loading_screen, context=self._we)

    @property
    def your_selection_header(self):
        return self._your_selection_header_type(self._your_selection_header, context=self._we)

    @property
    def overask(self):
        return self._overask_type(selector=self._overask_item, context=self._we)

    def wait_for_overask_panel(self, expected_result=True, timeout=10):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._overask_item, context=self._we, timeout=0),
            name=f'Overask to be {expected_result}',
            expected_result=expected_result,
            timeout=timeout)

    @property
    def overask_trader_section(self):
        return self._overask_trader_section_type(selector=self._betslip_sections_list, context=self._we)

    @property
    def overask_warning(self):
        return self.betnow_section.overask_warning

    def wait_for_overask_warning(self, expected_result=True, timeout=3):
        return wait_for_result(
            lambda: self.betnow_section.overask_warning != '',
            name=f"Overask warning displayed status to be {expected_result}",
            timeout=timeout)

    def wait_for_overask_message_to_change(self, previous_message='', timeout=10):
        return self.betnow_section.wait_for_overask_message_to_change(previous_message, timeout)

    @property
    def selections_count(self):
        selections_count = self.your_selection_header.count
        return selections_count if selections_count else '0'

    @property
    def your_selections_label(self):
        return self.your_selection_header.title_text

    @property
    def balance_button(self):
        return ButtonBase(selector=self._betslip_balance_button, timeout=1)

    def has_balance_button(self, expected_result=True, timeout=3):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._betslip_balance_button, timeout=0) is not None,
            name=f'"Balance" button shown status to be "{expected_result}"',
            timeout=timeout,
            expected_result=expected_result)

    def _odds_counted(self):
        if vec.betslip.BETSLIP_SINGLES_NAME in self.betslip_sections_list.keys():
            section = self.betslip_sections_list[vec.betslip.BETSLIP_SINGLES_NAME]
            return all(section[item].odds != '' for item in section.keys() if not section[item].is_suspended(timeout=0))
        else:
            return False

    def wait_for_betslip_widget_displayed(self, open_status: bool = True, timeout: (int, float) = 20):
        """
        Waits for betslip widget to be opened or closed
        Just specify open status as a parameter, True goes for open, False - for close
        """
        return wait_for_result(
            lambda: 'is-visible' in self.get_attribute('class') and self.is_displayed() and (
                        self._find_element_by_selector(
                            selector=self._no_selections_message, timeout=0) is not None or self._odds_counted()),
            name='Waiting for Betslip form displayed',
            expected_result=open_status,
            timeout=timeout,
            bypass_exceptions=()
        )

    def _wait_active(self, timeout=15):
        self._we = self._find_myself()
        try:
            result = self.wait_for_betslip_widget_displayed(open_status=True, timeout=timeout)
        except (StaleElementReferenceException, VoltronException):
            self._we = self._find_myself()
            result = self.wait_for_betslip_widget_displayed(open_status=True, timeout=timeout / 2)
        if not result:
            raise VoltronException(f'Timeout waiting for "{self.__class__.__name__}" content')

    @property
    def close_button(self):
        return CloseButton(selector=self._close_button, context=self._we, timeout=3)

    @property
    def betslip_title(self):
        return TextBase(selector=self._page_title, context=self._we).name

    def has_deposit_form(self, expected_result=True, timeout=30):
        return wait_for_result(
            lambda: self._find_element_by_selector(
                selector=self._betslip_deposit, timeout=0) is not None and self._find_element_by_selector(
                selector=self._betslip_deposit, timeout=0).is_displayed(),
            name=f'"Quick Deposit" section shown status to be: "{expected_result}"',
            timeout=timeout,
            expected_result=expected_result)

    @property
    def quick_deposit(self):
        return GVCQuickDeposit(selector=self._betslip_deposit, context=self._we)

    def has_deposit_link(self, timeout=1, expected_result=True):
        if not self.has_balance_button(expected_result=expected_result, timeout=1):
            return False

        self.balance_button.click()
        wait_for_result(lambda: self._find_element_by_selector(selector=self._quick_deposit_option, timeout=3),
                        timeout=3,
                        name='"Deposit" option to be shown')
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._quick_deposit_option,
                                                   context=self._we,
                                                   timeout=0) is not None,
            name=f'Link status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)

    @property
    def quick_deposit_link(self):
        self.balance_button.click()
        wait_for_result(lambda: self._find_element_by_selector(selector=self._quick_deposit_option, timeout=3),
                        timeout=3,
                        name='"Deposit" option to be shown')
        return ButtonBase(selector=self._quick_deposit_option, context=self._we)

    @property
    def hide_balance_option(self):
        self.balance_button.click()
        wait_for_result(lambda: self._find_element_by_selector(selector=self._hide_balance_option, timeout=3),
                        timeout=3,
                        name='"Hide Balance" option to be shown')
        return ButtonBase(selector=self._hide_balance_option, context=self._we)

    @property
    def betslip_sections_list(self):
        return self._betslip_sections_list_type(selector=self._betslip_sections_list, context=self._we, timeout=3)

    @property
    def betnow_section(self):
        return self._betnow_section_type(selector=self._betnow_section, context=self._we, timeout=3)

    @property
    def bet_now_button(self):
        return self.betnow_section.bet_now_button

    def has_bet_now_button(self, timeout=1, expected_result=True):
        return self.betnow_section.has_bet_now_button(timeout=timeout, expected_result=expected_result)

    @property
    def make_quick_deposit_button(self):
        return self.betnow_section.make_quick_deposit_button

    def has_make_quick_deposit_button(self, timeout=1, expected_result=True):
        return self.betnow_section.has_make_quick_deposit_button(timeout, expected_result)

    @property
    def deposit_and_place_bet_button(self):
        return self.betnow_section.deposit_and_place_bet_button

    def has_deposit_and_place_bet_button(self, timeout=1, expected_result=True):
        return self.betnow_section.has_deposit_and_place_bet_button(timeout, expected_result)

    @property
    def deposit_button(self):
        return self.betnow_section.deposit_button

    def has_deposit_button(self, timeout=1, expected_result=True):
        return self.betnow_section.has_deposit_button(timeout, expected_result)

    @property
    def info_panel(self):
        return InfoPanel(selector=self._betslip_error_message, context=self._we)

    @property
    def error(self):
        return self.betnow_section.error

    @property
    def count_down_message(self):
        return self.betnow_section.count_down_message

    @property
    def timer(self):
        return self.betnow_section.timer

    def wait_for_error(self, timeout=5, expected_result=True):
        return self.betnow_section.wait_for_error(timeout=timeout, expected_result=expected_result)

    def wait_for_specified_error(self, expected_message, timeout=5):
        return wait_for_result(lambda: self.wait_for_error(timeout=0) == expected_message,
                               name=f'Wait until "{expected_message}" will appear',
                               timeout=timeout)

    @property
    def warning_message(self):
        return self._wait_for_not_empty_web_element_text(selector=self._betslip_error_message, timeout=3)

    @property
    def price_change_warning_message(self):
        return self._wait_for_not_empty_web_element_text(selector=self._price_change_warning_message, timeout=3)

    @property
    def suspended_account_warning_message(self):
        return self._find_element_by_selector(selector=self._suspended_account_warning_message, context=self._we,
                                              timeout=3)

    @property
    def bet_amount_warning_message(self):
        return self._wait_for_not_empty_web_element_text(selector=self._incorrect_bet_amount_warning_message,
                                                         context=self._we,
                                                         timeout=3)

    def wait_for_warning_message(self, timeout=5, expected_result=True):
        wait_for_result(lambda: self._find_element_by_selector(selector=self._betslip_error_message, timeout=0),
                        timeout=timeout,
                        name='Error message to be shown',
                        expected_result=expected_result)
        return self.warning_message

    def wait_for_warning_message_text(self, text, timeout=5):
        self.wait_for_warning_message()
        return wait_for_result(lambda: self.warning_message == text,
                               timeout=timeout,
                               name=f'Warning message: "{text}" to be shown')

    @property
    def odds_boost_header(self):
        return self._odds_boost_header_type(selector=self._odds_boost_header, context=self._we)

    @property
    def has_odds_boost_header(self):
        odds_boost_header = self._find_element_by_selector(selector=self._odds_boost_header, timeout=1)
        return odds_boost_header.is_displayed() if odds_boost_header else False

    @property
    def remove_all_button(self):
        return ButtonBase(selector=self._remove_all_button, context=self._we)

    # empty betslip:

    @property
    def no_selections_title(self):
        return self._wait_for_not_empty_web_element_text(selector=self._no_selections_title, timeout=5)

    @property
    def no_selections_message(self):
        return self._wait_for_not_empty_web_element_text(selector=self._no_selections_message, timeout=5)

    def has_start_betting_button(self, expected_result=True, timeout=3):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._start_betting_button, timeout=0) is not None,
            name=f'"Start Betting" button shown status to be "{expected_result}"',
            timeout=timeout,
            expected_result=expected_result)

    @property
    def start_betting_button(self):
        return ButtonBase(selector=self._start_betting_button, context=self._we)

    @property
    def total_stake(self):
        return self.betnow_section.total_stake

    @property
    def total_stake_currency(self):
        return self.betnow_section.total_stake_currency

    @property
    def total_estimate_returns(self):
        return self.betnow_section.total_estimate_returns

    @property
    def total_estimate_returns_currency(self):
        return self.betnow_section.total_estimate_returns_currency

    @property
    def keyboard(self):
        return self.betnow_section.keyboard

    @property
    def quick_stake_panel(self):
        return self.betnow_section.quick_stake_panel

    @property
    def confirm_overask_offer_button(self):
        return self.betnow_section.confirm_overask_offer_button

    @property
    def cancel_button(self):
        return self.betnow_section.cancel_button

    def has_cancel_button(self, expected_result=True, timeout=2, poll_interval=0.3):
        return self.betnow_section.has_cancel_button(expected_result=expected_result, timeout=timeout,
                                                     poll_interval=poll_interval)

    def has_max_payout_msg(self, timeout=3, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._max_payout_msg, timeout=0) is not None,
            name=f'max payout info to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)

    def has_max_payout_link(self, timeout=3, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._max_payout_link, timeout=0) is not None,
            name=f'max payout link to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)


class LottoBetSlip(BetSlip):
    _max_payout_info = 'xpath=.//*[contains(@class, "maxpay-info-msg")]'
    _max_payout_link = 'xpath=.//*[contains(@class, "maxpay-info-msg")]//*[contains(@class, "max-payout")]//span[position() = 2]/a'
    _betslip_sections_list_type = LottoBetSlipSectionsList

    def wait_for_betslip_widget_displayed(self, open_status=True, timeout=7):
        """Waits for betslip widget to be opened of closed
           Just specify open status as a parameter, True goes for open, False - for close"""
        return wait_for_result(
            lambda: self.is_displayed(),
            name='Betslip widget displayed',
            expected_result=open_status,
            timeout=timeout
        )

    @property
    def max_payout_info(self):
        return self._get_webelement_text(selector=self._max_payout_info, timeout=10)

    @property
    def max_payout_link(self):
        return LinkBase(selector=self._max_payout_link, timeout=10)

    def has_max_payout_info(self, timeout=3, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._max_payout_info, timeout=0) is not None,
            name=f'max payout info to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)
