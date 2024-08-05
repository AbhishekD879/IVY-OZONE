from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException

from voltron.pages.shared import get_device_properties
from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.deposit_amount_form import DepositAmountFormOnBetslip
from voltron.pages.shared.components.info_panel import InfoPanel
from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.pages.shared.components.primitives.inputs import InputBase
from voltron.pages.shared.components.primitives.keyboard_input import KeyboardInputBase
from voltron.pages.shared.components.primitives.text_labels import TextBase
from voltron.pages.shared.contents.betslip.quick_deposit_payment_dropdown import PaymentAccountDropDown
from voltron.utils.waiters import wait_for_result


class FormHeader(ComponentBase):

    @property
    def text(self):
        return self._get_webelement_text(we=self._we)


class BetSlipQuickDeposit(ComponentBase):
    _header = 'xpath=.//*[@data-crlat="betslipDepositSelectCardTitle"]'
    _form_header = 'xpath=.//*[@data-crlat="qDFormHeader"]'
    _deposit_required_fields = 'xpath=.//*[@data-crlat="depositRequiredFields"]'
    _deposit_limits_link = 'xpath=.//*[@data-crlat="limits" or contains(@href, "limits")]'
    _expiry_date = 'xpath=.//*[@data-crlat="expDate.value"]'
    _cvv = 'xpath=.//*[@data-crlat="input.cvv"]'
    _cvv_field = 'xpath=.//*[@data-crlat="input-field.cvv"]'
    _cvv_validation_error = 'xpath=.//*[@data-crlat="errorValidationCV2"]'
    _amount_form = 'xpath=.//*[@data-crlat="stake.amountInputForm"]'
    _amount_container = 'xpath=.//*[contains(@data-crlat, "quickDeposit.amount")]'
    _card_id = 'xpath=.//*[@data-crlat="cardId" or @class="card-title"]'  # BMA
    _info_panel = 'xpath=.//*[@data-crlat="betslipDeposit.textMsg"]'
    _expanded = 'xpath=.//*[@data-crlat="quickDepositFormExpanded"]'
    _close_button = 'xpath=.//*[@data-crlat="buttonClose"]'
    _error_deposit_amount = 'xpath=.//*[@data-crlat="errorDepositAmount"]'
    _minus_button = 'xpath=.//*[@data-crlat="minusBtn"]'
    _plus_button = 'xpath=.//*[@data-crlat="plusBtn"]'
    _payment_account_dropdown = 'xpath=.//*[@data-crlat="paymentAccounts"]'
    _payment_account_type = PaymentAccountDropDown
    _warning_panel = 'xpath=.//div[@data-crlat="depositInfo.message"]'

    @property
    def _cvv_type(self):
        device_type = get_device_properties()['type']
        if device_type in ['mobile', 'tablet', 'desktop']:
            return InputBase
        return KeyboardInputBase

    def wait_info_panels(self, timeout=4):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._info_panel, timeout=0).is_displayed(),
                               name='Info panel shown',
                               bypass_exceptions=(NoSuchElementException, StaleElementReferenceException, AttributeError),
                               timeout=timeout)

    def is_expanded(self, expected_result=True, timeout=2):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._expanded, timeout=0),
                               expected_result=expected_result,
                               name=f'Quick deposit expanded status to be {expected_result}',
                               timeout=timeout)

    @property
    def info_panels_text(self):
        self.wait_info_panels()
        info_texts = self.info_panel.texts
        return info_texts

    @property
    def info_panel(self):
        return InfoPanel(selector=self._info_panel, context=self._we, timeout=30)

    @property
    def warning_panel(self):
        return InfoPanel(selector=self._warning_panel, context=self._we, timeout=15)

    @property
    def header(self):
        return self._get_webelement_text(selector=self._header, timeout=2)

    @property
    def form_header(self):
        return FormHeader(selector=self._form_header, timeout=1)

    @property
    def deposit_required_fields(self):
        return self._get_webelement_text(selector=self._deposit_required_fields, timeout=1)

    @property
    def deposit_limits_link(self):
        return ButtonBase(selector=self._deposit_limits_link, context=self._we)

    @property
    def current_account(self):
        return TextBase(selector=self._card_id, context=self._we, timeout=2).name

    @property
    def payment_account_dropdown(self):
        dropdown_we = self._find_element_by_selector(selector=self._payment_account_dropdown, context=self._we, timeout=1)
        return self._payment_account_type(web_element=dropdown_we)

    def has_payment_account_dropdown(self, timeout=1, expected_result=True) -> bool:
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._payment_account_dropdown,
                                                   timeout=0) is not None,
            name=f'Payment dropdown status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)

    @property
    def amount_form(self):
        return DepositAmountFormOnBetslip(selector=self._amount_form, context=self._we)

    @property
    def minus_button(self):
        return ButtonBase(selector=self._minus_button, context=self._we)

    @property
    def plus_button(self):
        return ButtonBase(selector=self._plus_button, context=self._we)

    @property
    def amount_validation_error(self):
        return self._get_webelement_text(selector=self._error_deposit_amount, timeout=1)

    def clear_cvv(self):
        device_type = get_device_properties()['type']
        if device_type in ['mobile', 'tablet', 'desktop']:
            self.cvv.value = ''
        else:
            self.cvv.clear()

    def enter_cvv(self, value):
        self.cvv.send_keys(value)

    @property
    def cvv(self):
        return self._cvv_type(selector=self._cvv, context=self._we)

    @property
    def cvv_field(self):
        return self._cvv_type(selector=self._cvv_field, context=self._we)

    @property
    def cvv_validation_error(self):
        return self._get_webelement_text(selector=self._cvv_validation_error, context=self._we, timeout=1)

    @property
    def cvv_text(self):
        return wait_for_result(lambda: self.cvv.get_attribute('value'),
                               name='CVV value to appear',
                               timeout=2)

    @property
    def deposit_amount_text(self):
        return wait_for_result(lambda: self.amount_form.input.get_attribute('value'),
                               name='Deposit amount value to appear',
                               timeout=2)

    @property
    def card_id(self):
        return self._get_webelement_text(selector=self._card_id)

    @property
    def close_button(self):
        return ButtonBase(selector=self._close_button, context=self._we)
