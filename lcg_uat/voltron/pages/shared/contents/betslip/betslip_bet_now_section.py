import re

from voltron.pages.shared import get_driver
from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.keyboard.mobile_keyboard import Keyboard
from voltron.pages.shared.components.primitives.buttons import ButtonBase, BetNowButton
from voltron.pages.shared.components.primitives.buttons import SpinnerButtonBase
from voltron.pages.shared.components.quick_stake_panel import QuickStakePanel
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.waiters import wait_for_result
from voltron.pages.shared.components.primitives.text_labels import LinkBase


class BetNowSection(ComponentBase):
    _confirm_accept_overask_offer = 'xpath=.//*[@data-crlat="ovAccept"]'
    _total_stake = 'xpath=.//*[@data-crlat="totalStake"]'
    _total_est_returns = 'xpath=.//*[@data-crlat="totalEstReturns"]'
    _place_bet_button = 'xpath=.//*[@data-uat="betNowBtn"]'
    _continue_btn = 'xpath=.//*[@data-crlat="continueOveraskBtn"]'
    _go_betting_btn = 'xpath=.//*[@data-crlat="doneDeclinedOveraskBtn"]'
    _cancel_btn = 'xpath=.//*[@data-crlat="ovCancel"]'
    _overask_warning = 'xpath=.//*[@data-crlat="stateMsg"]'
    _error = 'xpath=.//*[@data-crlat="bs.Err"]'
    _make_quick_deposit_button = 'xpath=.//*[@data-crlat="makeQD"]'
    _deposit_and_place_bet_button = 'xpath=.//*[@data-crlat="depositAndPlaceBetBtn"]'
    _keyboard = 'xpath=.//*[@data-crlat="betslip.keyboard"]'
    _quick_stake_panel = 'xpath=.//*[@data-crlat="quickStakePanel"] | .//*[@data-crlat="bsFoot"]'
    _count_down_message = 'xpath=.//*[@data-crlat="countDownTimerMessage"]'
    _timer = 'xpath=.//*[@data-crlat="timer"]'
    _german_tax_message = 'xpath=.//*[@data-crlat="taxMessage"]'
    _deposit_button = 'xpath=.//*[@data-crlat="depositBtn"]'

    @property
    def keyboard(self):
        return Keyboard(selector=self._keyboard, context=self._we, timeout=2)

    @property
    def quick_stake_panel(self):
        return QuickStakePanel(selector=self._quick_stake_panel, context=self._we, timeout=2)

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
        raise VoltronException('Failed parsing amount string: "%s"' % est_returns)

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
        raise VoltronException('Failed parsing amount string: "%s"' % est_returns)

    def has_german_tax_message(self, timeout=1, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._german_tax_message, timeout=0) is not None,
            name=f'"Tax message" message to be "{expected_result}"', expected_result=expected_result,
            timeout=timeout)

    @property
    def german_tax_message_text(self):
        return self._get_webelement_text(selector=self._german_tax_message)

    @property
    def bet_now_button(self):
        return BetNowButton(selector=self._place_bet_button, context=self._we, timeout=3)

    @property
    def go_betting_button(self):
        return BetNowButton(selector=self._go_betting_btn, context=self._we, timeout=3)

    def has_bet_now_button(self, timeout=1, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._place_bet_button,
                                                   timeout=0) is not None,
            name=f'Bet Now button status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)

    @property
    def confirm_overask_offer_button(self):
        return SpinnerButtonBase(selector=self._confirm_accept_overask_offer, context=self._we)

    @property
    def continue_button(self):
        return ButtonBase(selector=self._continue_btn, context=self._we)

    def has_cancel_button(self, expected_result=True, timeout=2, poll_interval=0.3):
        result = wait_for_result(
            lambda: self._find_element_by_selector(selector=self._cancel_btn, timeout=0) is not None,
            name='Cancel button to appear',
            expected_result=expected_result,
            timeout=timeout,
            poll_interval=poll_interval)
        return result

    @property
    def cancel_button(self):
        return ButtonBase(selector=self._cancel_btn, context=self._we)

    @property
    def make_quick_deposit_button(self):
        return ButtonBase(selector=self._make_quick_deposit_button, context=self._we, timeout=5)

    def has_make_quick_deposit_button(self, timeout=1, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._make_quick_deposit_button,
                                                   timeout=0) is not None,
            name=f'Quick deposit button status to be "{expected_result}"',
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
    def error(self):
        wait_for_result(lambda: self._get_webelement_text(selector=self._error, timeout=0) != '',
                        name='Error message to appear',
                        timeout=5,
                        poll_interval=1)
        return self._get_webelement_text(selector=self._error, timeout=0)

    def wait_for_error(self, timeout=5, expected_result=True):
        wait_for_result(lambda: self._find_element_by_selector(selector=self._error, timeout=0),
                        timeout=timeout,
                        name='Error message to appear',
                        expected_result=expected_result)
        return self.error

    def wait_for_overask_message_to_change(self, previous_message='', timeout=10):
        result = wait_for_result(lambda: self._get_webelement_text(selector=self._overask_warning,
                                                                   context=get_driver(),
                                                                   timeout=0) != previous_message,
                                 name='Overask warning text to change',
                                 timeout=timeout,
                                 poll_interval=0.3)
        return result

    @property
    def overask_warning(self):
        return self._get_webelement_text(selector=self._overask_warning, timeout=1)

    def has_overask_warning(self, expected_result=True, timeout=5):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._overask_warning, timeout=0) is not None,
            timeout=timeout,
            expected_result=expected_result,
            name=f'Overask warning message presence status in {self.__class__.__name__} to be {expected_result}')

    @property
    def count_down_message(self):
        return self._get_webelement_text(selector=self._count_down_message, timeout=10)

    @property
    def timer(self):
        return wait_for_result(lambda: self._get_webelement_text(selector=self._timer),
                               name='Countdown timer to appear',
                               timeout=5)

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
