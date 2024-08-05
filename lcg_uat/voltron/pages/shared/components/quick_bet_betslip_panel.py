from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.info_panel import InfoPanel
from voltron.pages.shared.components.keyboard.mobile_keyboard import Keyboard
from voltron.pages.shared.components.payment_accounts import PaymentAccounts
from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.pages.shared.components.quick_deposit_button import QuickDepositButton
from voltron.pages.shared.contents.betslip.betslip_quick_deposit import BetSlipQuickDeposit
from voltron.utils.waiters import wait_for_result


class DepositAndPlaceButton(QuickDepositButton):
    pass


class QuickDeposit(BetSlipQuickDeposit):
    _close_button = 'xpath=.//*[@data-crlat="closeButton"]'
    _deposit_limits_link = 'xpath=.//*[@data-crlat="limits"]'
    _info_panel = 'xpath=.//*[@data-crlat="infPan.msg"]'

    _card_icon = 'xpath=.//*[@data-crlat="cardIcon"]'
    _select_card_message = 'xpath=.//*[@data-crlat="selectCard"]'
    _all_cards = 'xpath=.//*[@data-crlat="userCreditCards"]'
    _deposit_and_place_bet_button = 'xpath=.//*[@data-crlat="quickbet.depositAndBet"]'
    _keyboard = 'xpath=.//*[@data-crlat="betslip.keyboard"]'
    _deposit = 'xpath=.//*[@data-crlat="quickDeposit.makeDeposit"]'
    _quick_deposit_panel = 'xpath=.//*[@data-crlat="quickDepositPanel"]'
    _quick_stake_panel = 'xpath=.//*[@data-crlat="quickStakePanel"]'
    _title = 'xpath=.//*[@data-crlat="header.title"]'
    _card_section = 'xpath=.//*[@data-crlat="paymentAccounts"]'
    _drop_down = 'xpath=.//*[@data-crlat="arrow.select"]'

    @property
    def card_icon(self):
        return self._find_element_by_selector(selector=self._card_icon)

    @property
    def select_card_message(self):
        return self._find_element_by_selector(selector=self._select_card_message)

    @property
    def close_button(self):
        return ButtonBase(selector=self._close_button, context=self._we)

    @property
    def deposit_limits_link(self):
        return ButtonBase(selector=self._deposit_limits_link, context=self._we)

    @property
    def drop_down_arrow(self):
        return ButtonBase(selector=self._drop_down, context=self._we)

    @property
    def info_panels_text(self):
        return self.info_panels.texts

    @property
    def info_panels(self):
        return InfoPanel(selector=self._info_panel, context=self._we, timeout=15)

    def wait_for_message_to_change(self, previous_message='', timeout=10):
        result = wait_for_result(lambda: self._get_webelement_text(selector=self._info_panel, timeout=0) != previous_message,
                                 name='Waiting for warning text to change',
                                 timeout=timeout,
                                 poll_interval=0.3)
        return result

    def wait_for_quick_deposit_info_panel(self, expected_result=True, timeout=15):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._info_panel,
                                                                      timeout=0) is not None and self._find_element_by_selector(selector=self._info_panel,
                                                                                                                                timeout=0).is_displayed(),
                               name='Quick Bet info panel to be displayed',
                               expected_result=expected_result,
                               timeout=timeout)

    @property
    def deposit_and_place_bet_button(self):
        return DepositAndPlaceButton(selector=self._deposit_and_place_bet_button, context=self._we)

    @property
    def keyboard(self):
        return Keyboard(selector=self._keyboard, context=self._we, timeout=2)

    @property
    def deposit_button(self):
        return ButtonBase(selector=self._deposit, context=self._we)

    @property
    def accounts(self):
        return PaymentAccounts(selector=self._quick_deposit_panel)

    def wait_for_quick_stake_panel(self, expected_result=True, timeout=0.5):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._quick_stake_panel,
                                                                      timeout=0) is not None and self._find_element_by_selector(selector=self._quick_stake_panel,
                                                                                                                                timeout=0).is_displayed(),
                               name='Quick Stake panel to be displayed',
                               expected_result=expected_result,
                               timeout=timeout)

    @property
    def title(self):
        return self._get_webelement_text(selector=self._title)

    @property
    def card_section(self):
        return ComponentBase(selector=self._card_section)
