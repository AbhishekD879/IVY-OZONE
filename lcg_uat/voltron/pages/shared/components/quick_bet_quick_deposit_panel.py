from voltron.pages.coral.components.primitives.quick_deposit_button import CoralDepositAndPlaceButton
from voltron.pages.shared import get_driver
from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.info_panel import InfoPanel
from voltron.pages.shared.components.keyboard.gvc_keyboard import GVCKeyboard
from voltron.pages.shared.components.keyboard.mobile_keyboard import Key
from voltron.pages.shared.components.keyboard.mobile_keyboard import Keyboard
from voltron.pages.shared.components.payment_accounts import PaymentAccounts
from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.pages.shared.contents.deposit.deposit_base import GVCDepositIframeBase
from voltron.pages.shared.contents.deposit.primitives.input import GVCDepositInput
from voltron.utils.helpers import switch_to_main_page
from voltron.utils.waiters import wait_for_result


class GVCQuickStakeKey(Key):
    @property
    def name(self):
        return self._get_webelement_text(we=self._we)


class GVCQuickStakePanel(Keyboard):
    _item = 'xpath=.//*[contains(@class, "md-button")]'
    _list_item_type = GVCQuickStakeKey


class GVCQuickDepositHeader(ComponentBase):
    _title = 'xpath=.//*[@data-crlat="text"]'
    _close_button = 'xpath=.//*[@data-crlat="closeButton"]'

    @property
    def title(self):
        return self._get_webelement_text(selector=self._title)

    @property
    def close_button(self):
        return ButtonBase(selector=self._close_button, context=self._we)

    def has_close_button(self, timeout=1, expected_result=True):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._close_button, timeout=0) is not None,
                               name=f'Close button status to be "{expected_result}"',
                               expected_result=expected_result,
                               timeout=timeout)

    def scroll_to_we(self, web_element=None):
        """
        Bypassing scroll as element in a view
        """
        pass


class GVCQuickDeposit(GVCDepositIframeBase):
    _iframe = 'xpath=.//iframe[contains(@class, "quick-deposit__iframe")]'
    _close_button = 'xpath=.//*[contains(@class, "close-button") or contains(@class, "ui-close") or contains(@data-crlat, "closeButton")]'
    _notification_panel = 'xpath=.//*[@data-crlat="bs.ntfErr"]'
    _warning_panel = 'xpath=.//*[@class="info-msg"]'
    _warning_icon = 'xpath=.//*[@class="theme-info"]'
    _deposit_limit_error = 'xpath=.//*[@ng-show="rgLimitsErrorDetails"]'
    _deposit_amount_error = 'xpath=.//*[@class="error-container"]/*[@ng-messages="form.navamount.$error"]'
    _cvv_error = 'xpath=.//*[@ng-messages="ccinputform.cvv2.$error"]'
    _accounts = 'xpath=.//*[@class="options-list-dropdown"]'
    _cvv_2 = 'xpath=.//md-input-container[./input[@id="cvv2"]]'
    _cvv_2_type = GVCDepositInput
    _minus_button = 'xpath=.//*[@class="grid-block"]//button[@aria-label="minus"]'
    _amount = 'xpath=.//md-input-container[./input[@id="navamount"]] | .//md-input-container[./input[@id="amountInTxnCurrency"]]'
    _amount_type = GVCDepositInput
    _plus_button = 'xpath=.//*[@class="grid-block"]//button[@aria-label="plus"]'
    _quick_stake_panel = 'xpath=.//*[@class="amount-btns flex"]'
    _quick_stale_panel_type = GVCQuickStakePanel
    _keyboard = 'xpath=.//*[@id="keyboard-target"][*]'
    _total_stake_value = 'xpath=.//*[@class="total-stake"]/p/span'
    _potential_returns_value = 'xpath=.//*[@class="total-stake"]/p[@class="potential-returns"]/span'
    _deposit_and_place_bet_button = 'xpath=.//button[contains(@class,"btn md-button")]'
    _header = 'xpath=.//*[@data-crlat="header"]'
    _info_panel = 'xpath=.//*[@data-crlat="bs.ntfErr"]'
    _header_type = GVCQuickDepositHeader
    _deposit = 'xpath=.//button[contains(@class,"btn md-button")]'
    _amount_currency_label = 'xpath=.//md-input-container[./input[@id="navamount"]]//*[@class="currency-symbol"]'

    @property
    def notification_panel(self):
        """
        This panel located outside of iFrame
        """
        switch_to_main_page()
        return self._get_webelement_text(selector=self._notification_panel, context=get_driver(), timeout=2)

    @property
    def warning_panel(self):
        return self._get_webelement_text(selector=self._warning_panel, context=get_driver(), timeout=2)

    @property
    def warning_icon(self):
        return ButtonBase(selector=self._warning_icon, context=get_driver(), timeout=2)

    @property
    def deposit_limit_error(self):
        return self._wait_for_not_empty_web_element_text(selector=self._deposit_limit_error,
                                                         context=get_driver(), timeout=15)

    @property
    def deposit_amount_error(self):
        return self._wait_for_not_empty_web_element_text(selector=self._deposit_amount_error, context=get_driver(), timeout=2)

    @property
    def cvv_error(self):
        return self._wait_for_not_empty_web_element_text(selector=self._cvv_error, context=get_driver(), timeout=2)

    @property
    def accounts(self):
        return PaymentAccounts(selector=self._accounts, context=get_driver(), timeout=2)

    @property
    def cvv_2(self):
        return self._cvv_2_type(selector=self._cvv_2, context=get_driver(), timeout=2)

    @property
    def minus_button(self):
        return ButtonBase(selector=self._minus_button, context=get_driver(), timeout=2)

    @property
    def amount(self):
        return self._amount_type(selector=self._amount, context=get_driver(), timeout=2)

    @property
    def plus_button(self):
        return ButtonBase(selector=self._plus_button, context=get_driver(), timeout=2)

    @property
    def quick_stake_panel(self):
        return self._quick_stale_panel_type(selector=self._quick_stake_panel, context=get_driver(), timeout=2)

    @property
    def keyboard(self):
        return GVCKeyboard(selector=self._keyboard, context=get_driver(), timeout=2)

    def has_keyboard(self, expected_result=True, timeout=15):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._keyboard, timeout=0, context=get_driver()) is not None,
            expected_result=expected_result,
            name='Keyboard to be displayed',
            timeout=timeout)

    @property
    def total_stake_value(self):
        return self._get_webelement_text(selector=self._total_stake_value, context=get_driver(), timeout=2)

    @property
    def potential_returns_value(self):
        return self._get_webelement_text(selector=self._potential_returns_value, context=get_driver(), timeout=2)

    @property
    def deposit_and_place_bet_button(self):
        return CoralDepositAndPlaceButton(selector=self._deposit_and_place_bet_button, context=get_driver(), timeout=2)

    def get_iframe_url(self):
        return ComponentBase(self._iframe, timeout=2).get_attribute('src')

    @property
    def header(self):
        return self._header_type(selector=self._header, context=self._we, timeout=1)

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
    def info_panels_text(self):
        return self.info_panels.texts

    @property
    def info_panels(self):
        return InfoPanel(selector=self._info_panel, context=self._we, timeout=15)

    @property
    def deposit_button(self):
        return ButtonBase(selector=self._deposit, context=self._we)

    @property
    def currency(self):
        return self._get_webelement_text(selector=self._amount_currency_label, context=get_driver(), timeout=2)
