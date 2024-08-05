import re

import voltron.environments.constants as vec
from voltron.pages.ladbrokes.contents.betslip.betslip_overlay_notification import BetSlipOverlayNotification
from voltron.pages.shared import get_driver
from voltron.pages.shared.components.keyboard.mobile_keyboard import Keyboard
from voltron.pages.shared.components.primitives.buttons import ButtonBase, BetNowButton
from voltron.pages.shared.components.primitives.buttons import SpinnerButtonBase
from voltron.pages.shared.components.quick_stake_panel import QuickStakePanel
from voltron.pages.shared.contents.betslip.betslip import BetSlip, LottoBetSlip
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.waiters import wait_for_result


class BetSlipLadbrokes(BetSlip):
    _place_bet_button = 'xpath=.//*[@data-uat="betNowBtn"]'
    _total_stake = 'xpath=.//*[@data-crlat="totalStake"]'
    _total_est_returns = 'xpath=.//*[@data-crlat="totalEstReturns"]'
    _bs_top_overlay_notification = 'xpath=.//*[@data-crlat="bsNotification"]'
    _error = 'xpath=.//*[@data-crlat="bs.Err"]'
    _make_quick_deposit_button = 'xpath=.//*[@data-crlat="makeQD"]'
    _deposit_and_place_bet_button = 'xpath=.//*[@data-crlat="depositAndPlaceBetBtn"]'
    _deposit_button = 'xpath=.//*[@data-crlat="depositBtn"]'
    _keyboard = 'xpath=.//*[@data-crlat="betslip.keyboard"]'
    _timer = 'xpath=.//*[@data-crlat="timer"]'
    _count_down_message = 'xpath=.//*[@data-crlat="timerMsg"]'
    _german_tax_message = 'xpath=.//*[@data-crlat="taxMessage"]'
    _quick_stake_panel = 'xpath=.//*[@data-crlat="quickStakePanel"]'
    _overask_warning = 'xpath=.//*[@data-crlat="stateMsg"]'
    _confirm_accept_overask_offer = 'xpath=.//*[@data-crlat="ovAccept"]'
    _cancel_btn = 'xpath=.//*[@data-crlat="ovCancel"]'
    _undo_button = 'xpath=.//*[@data-crlat="oUndoBtn"]'
    _market_name = 'xpath=.//*[@data-uat="marketName"]'

    def _odds_counted(self):
        if vec.betslip.BETSLIP_SINGLES_NAME in self.betslip_sections_list.keys():
            section = self.betslip_sections_list[vec.betslip.BETSLIP_SINGLES_NAME]
            return all(section[item].odds != '' for item in section.keys())
        else:
            return False

    @property
    def betnow_section(self):
        raise NotImplementedError(f'There is no "Bet Now" section for {self.__class__.__name__}')

    @property
    def bet_now_button(self):
        return BetNowButton(selector=self._place_bet_button, context=self._we, timeout=3)

    def has_bet_now_button(self, timeout=1, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._place_bet_button,
                                                   timeout=0) is not None,
            name=f'Bet Now button status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)

    @property
    def total_stake(self):
        result = self._wait_for_not_empty_web_element_text(selector=self._total_stake,
                                                           timeout=4,
                                                           name='Total stake to show up')
        if result:
            return self.strip_currency_sign(result).replace(',', '').replace('\n', '')
        return ''

    @property
    def total_stake_currency(self):
        est_returns = self._get_webelement_text(selector=self._total_stake)
        matched = re.match(r'^(\$|Kr|£|€)', est_returns)
        if matched:
            return matched.group(1)
        raise VoltronException(f'Failed parsing amount string: "{est_returns}"')

    @property
    def total_estimate_returns(self):
        est_returns = self._get_webelement_text(selector=self._total_est_returns)
        wait_for_result(lambda: est_returns != self._get_webelement_text(selector=self._total_est_returns),
                        name='Estimated Returns to Update',
                        timeout=1)
        est_returns = self._get_webelement_text(selector=self._total_est_returns)
        return self.strip_currency_sign(est_returns).replace(',', '')

    @property
    def total_estimate_returns_currency(self):
        est_returns = self._get_webelement_text(selector=self._total_est_returns)
        matched = re.match(r'^(\$|Kr|£|€)', est_returns)
        if matched:
            return matched.group(1)
        raise VoltronException(f'Failed parsing amount string: "{est_returns}"')

    def wait_for_top_notification(self, timeout=5, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._bs_top_overlay_notification, timeout=0) is not None,
            timeout=timeout,
            name=f'{self.__class__.__name__} - BetSlipOverlayNotification status to be {expected_result}',
            expected_result=expected_result)

    @property
    def top_notification(self):
        return BetSlipOverlayNotification(selector=self._bs_top_overlay_notification, context=self._we)

    @property
    def error(self):
        return self.wait_for_error(timeout=3)

    def wait_for_error(self, timeout=5, expected_result=True):
        return wait_for_result(lambda: self._get_webelement_text(selector=self._error, timeout=0),
                               timeout=timeout,
                               name=f'{self.__class__.__name__} - Error message status to be {expected_result}',
                               expected_result=expected_result)

    @property
    def keyboard(self):
        return Keyboard(selector=self._keyboard, context=self._we, timeout=2)

    @property
    def quick_stake_panel(self):
        return QuickStakePanel(selector=self._quick_stake_panel, context=self._we, timeout=2)

    @property
    def make_quick_deposit_button(self):
        return ButtonBase(selector=self._make_quick_deposit_button, context=self._we, timeout=5)

    def has_make_quick_deposit_button(self, timeout=1, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._make_quick_deposit_button,
                                                   timeout=0) is not None,
            name=f'{self.__class__.__name__} - Quick deposit button status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)

    @property
    def deposit_and_place_bet_button(self):
        return SpinnerButtonBase(selector=self._deposit_and_place_bet_button, context=self._we, timeout=3)

    def has_deposit_and_place_bet_button(self, timeout=1, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._deposit_and_place_bet_button,
                                                   timeout=0) is not None,
            name=f'Quick deposit button status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)

    @property
    def deposit_button(self):
        return SpinnerButtonBase(selector=self._deposit_button, context=self._we, timeout=3)

    def has_deposit_button(self, timeout=1, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._deposit_button,
                                                   timeout=0) is not None,
            name=f'Deposit button status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)

    @property
    def count_down_message(self):
        return self._get_webelement_text(selector=self._count_down_message, timeout=10)

    @property
    def timer(self):
        return wait_for_result(lambda: self._get_webelement_text(selector=self._timer),
                               name='Countdown timer to appear',
                               timeout=5)

    def has_german_tax_message(self, timeout=1, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._german_tax_message, timeout=0) is not None,
            name=f'"Tax message" message to be "{expected_result}"', expected_result=expected_result,
            timeout=timeout)

    @property
    def german_tax_message_text(self):
        if self.has_german_tax_message(timeout=1):
            return self._get_webelement_text(selector=self._german_tax_message)
        else:
            raise VoltronException('No German tax message found')

    @property
    def overask_warning(self):
        return self._get_webelement_text(selector=self._overask_warning, timeout=1)

    def wait_for_overask_warning(self, expected_result=True, timeout=3):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._overask_warning, timeout=0) is not None and self._find_element_by_selector(selector=self._overask_warning, timeout=0).is_displayed(),
            name=f"Overask warning displayed status to be {expected_result}",
            timeout=timeout)

    def wait_for_overask_message_to_change(self, previous_message='', timeout=10):
        result = wait_for_result(lambda: self._get_webelement_text(selector=self._overask_warning,
                                                                   context=get_driver(),
                                                                   timeout=0) != previous_message,
                                 name='Overask warning text to change',
                                 timeout=timeout,
                                 poll_interval=0.3)
        return result

    @property
    def confirm_overask_offer_button(self):
        return SpinnerButtonBase(selector=self._confirm_accept_overask_offer, context=self._we)

    @property
    def cancel_button(self):
        return ButtonBase(selector=self._cancel_btn, context=self._we)

    @property
    def undo_button(self):
        return ButtonBase(selector=self._undo_button, context=self._we)

    def has_cancel_button(self, expected_result=True, timeout=2, poll_interval=0.3):
        result = wait_for_result(
            lambda: self._find_element_by_selector(selector=self._cancel_btn, timeout=0) is not None,
            name='Cancel button to appear',
            expected_result=expected_result,
            timeout=timeout,
            poll_interval=poll_interval)
        return result


class LottoBetSlipLadbrokes(LottoBetSlip, BetSlipLadbrokes):
    pass
