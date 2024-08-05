from time import sleep
from voltron.pages.shared.components.payment_accounts import PaymentAccounts
from voltron.pages.shared.components.primitives.buttons import ButtonBase, ButtonNoScrollBase
from voltron.pages.shared.components.quick_stake_panel import QuickStakePanel
from voltron.pages.shared.contents.deposit.deposit_base import GVCDepositContent, GVCDepositIframeBase
from voltron.pages.shared.contents.deposit.primitives.input import GVCDepositInput
from voltron.utils.helpers import execute_in_iframe, perform_offset_mouse_click
from voltron.pages.shared import get_driver
from voltron.utils.waiters import wait_for_result
from tests.Common import Common


class GVCDeposit(GVCDepositContent, Common):
    _url_pattern = r'^http[s]?:\/\/.+\/deposit?'
    _amount = 'xpath=.//div[./input[@name="amount"]]'
    _amount_type = GVCDepositInput
    _card_holder = 'xpath=.//div[./input[@id="nameoncard"]] | .//input[@formcontrolname="nameOnCard"]'
    _card_holder_type = GVCDepositInput
    _card_number = 'xpath=.//div[./input[@name="cardNumber"]]'
    _card_number_type = GVCDepositInput
    _expiry_date = 'xpath=.//div[./input[@name="expiryDate"]]'
    _expiry_date_type = GVCDepositInput
    _cvv_2 = 'xpath=.//div[./input[@name="cvv"]]'
    _cvv_2_type = GVCDepositInput
    _deposit_button = 'xpath=.//*[contains(@class, "deposit-btn")]/button'
    _next_button = 'xpath=.//*[@class="btn btn-primary w-100"]'
    _user_input_amount_error = 'xpath=.//*[@id="userInputAmount-error"]'
    _amount_warning_msg = 'xpath=.//*[contains(@class,"content-message-container")]'

    @property
    def amount_warning_msg(self):
        return self._get_webelement_text(selector=self._amount_warning_msg)

    @property
    def is_warning_msg_came(self):
        return self._find_element_by_selector(selector=self._amount_warning_msg) is not None

    @property
    def amount(self):
        return self._amount_type(selector=self._amount)

    @property
    def card_holder(self):
        return self._card_holder_type(selector=self._card_holder)

    @property
    def card_number(self):
        return self._card_number_type(selector=self._card_number)

    @property
    def expiry_date(self):
        return self._expiry_date_type(selector=self._expiry_date)

    @property
    def cvv_2(self):
        return self._cvv_2_type(selector=self._cvv_2)

    @property
    def deposit_button(self):
        return ButtonBase(selector=self._deposit_button)

    @property
    def next_button(self):
        return ButtonBase(selector=self._next_button)

    def add_new_card_and_deposit(self, **kwargs):
        """
        Method should be used when user deposit first time with new card
        """
        self.form_values(**kwargs)
        if self.brand == "ladbrokes" and self.device_type == 'desktop':
            sleep(2)
        self.deposit_button.click()

    def form_values(self, **kwargs):
        amount = kwargs.get('amount', '22')
        card_holder = kwargs.get('card_holder')
        card_number = kwargs.get('card_number')
        expiry_date = kwargs.get('expiry_date')
        cvv_2 = kwargs.get('cvv_2')

        if card_holder:
            self.card_holder.input.value = card_holder
        if card_number:
            self.card_number.input.value = card_number
        if expiry_date:
            self.expiry_date.input.value = expiry_date
        if self.device_type == 'mobile':
            wait_for_result(lambda: self.next_button,
                            timeout=10)
            self.next_button.click()
        if cvv_2:
            self.cvv_2.input.value = cvv_2
        if amount:
            self.amount.input.value = amount

    def close(self):
        self.close_button.click()

    @property
    def user_input_amount_error(self):
        return self._find_element_by_selector(selector=self._user_input_amount_error, context=get_driver())


class CoralDepositMenu(GVCDepositIframeBase, GVCDeposit):
    _iframe = 'xpath=.//iframe[@id="quickdeposit-iframe"] | .//vn-iframe//iframe'
    _deposit_button = 'xpath=.//button[@class="btn md-button md-ink-ripple"]'
    _cvv_2 = 'xpath=.//div[@class="cvv-block"]'
    _amount = 'xpath=.//div[@class="amount-increase-decrease-block flex"]'
    _accounts = 'xpath=.//md-select[contains(@class, "payment-method-options")]'
    _plus_button = 'xpath=.//*[@class="grid-block"]//button[@aria-label="plus"]'
    _amount_clear = 'xpath=.//a[contains(@class,"clear")]'
    _quick_stake_panel = 'xpath=.//*[@class="amount-btns flex"]'
    _transaction_currency = 'xpath=.//*[@id="transactionCurrency"]'
    _transaction_tooltip = 'xpath=.//div[contains(@class,"currency-block")]/div[contains(@class,"cvv-info")]/span'
    _optional_bonus_code = 'xpath=.//div[@class="optional-bonus-text"]'
    _bonus_code = 'xpath=.//div[@class="bonus-input"]'
    _close_button = 'xpath=.//*[contains(@class, "ui-close")]'
    _deposit_title = 'xpath=.//*[contains(@class,"header-ctrl")]/*[contains(text(),"Deposit")]'
    _ok_button = 'xpath=.//*[@class="btn btn-alt md-button md-ink-ripple"]'

    def url_matcher(self):
        """There is no URL for quick deposit on Coral"""
        pass

    @execute_in_iframe(_iframe, timeout=3)
    def add_new_card_and_deposit(self, **kwargs):
        self.form_values(**kwargs)
        self.deposit_button.click(scroll_to=False)

    def form_values(self, **kwargs):
        amount = kwargs.get('amount')
        cvv_2 = kwargs.get('cvv_2')

        if cvv_2:
            self.cvv_2.input.value = cvv_2
        if amount:
            self.amount.input.value = amount

    @property
    def ok_button(self):
        return ButtonNoScrollBase(selector=self._ok_button)

    @execute_in_iframe(_iframe, timeout=3)
    def deposit_and_close(self, **kwargs):
        self.form_values(**kwargs)
        self.deposit_button.click(scroll_to=False)
        wait_for_result(lambda: self.ok_button.is_displayed(),
                        name='OK button is displayed',
                        timeout=5)
        self.ok_button.click(scroll_to=False)

    @property
    def deposit_button(self):
        return ButtonNoScrollBase(selector=self._deposit_button)

    @property
    def accounts(self):
        return PaymentAccounts(selector=self._accounts, context=get_driver())

    @property
    def plus_button(self):
        return ButtonBase(selector=self._plus_button, context=get_driver(), timeout=2)

    def close(self):
        perform_offset_mouse_click()

    @property
    def amount_clear(self):
        return self._find_element_by_selector(selector=self._amount_clear, context=get_driver())

    @property
    def quick_stake_panel(self):
        return QuickStakePanel(selector=self._quick_stake_panel, context=get_driver(), timeout=2)

    @property
    def transaction_currency(self):
        return self._find_element_by_selector(selector=self._transaction_currency, context=get_driver())

    @property
    def transaction_tooltip(self):
        return self._find_element_by_selector(selector=self._transaction_tooltip, context=get_driver())

    @property
    def optional_bonus_code(self):
        return self._find_element_by_selector(selector=self._optional_bonus_code, context=get_driver())

    @property
    def bonus_code(self):
        return self._find_element_by_selector(selector=self._bonus_code, context=get_driver())
