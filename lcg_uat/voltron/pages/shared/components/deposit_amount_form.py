import re

from selenium.webdriver.common.keys import Keys
from voltron.pages.shared import get_device_properties, get_driver

from voltron.pages.shared.components.amount_form import AmountForm
from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.pages.shared.components.primitives.inputs import InputBase
from voltron.pages.shared.components.primitives.keyboard_input import KeyboardInputBase
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.waiters import wait_for_result
from voltron.utils.js_functions import mouse_event_click as safari_click


class DepositInputBase(InputBase):

    def clear(self):
        self._we.clear()


class QuickAmountButton(ButtonBase):

    def click(self, scroll_to=True):
        self.scroll_to_we() if scroll_to else None
        if self.is_safari:
            safari_click(self._we)
        else:
            get_driver().execute_script("arguments[0].click();", self._we)


class QuickAmountSection(ComponentBase):
    _item = 'xpath=.//*[@data-crlat="addAmount"]'
    _list_item_type = QuickAmountButton


class DepositAmountForm(AmountForm):
    _amount = 'xpath=.//*[@data-crlat="value" or @data-crlat="enterAmount"]'
    _quick_amount_section = 'xpath=.//*[@data-crlat="quickAmountsButtons"]'
    _quick_amount_section_type = QuickAmountSection
    _amount_currency_label = 'xpath=.//*[@data-crlat="currencySymbol"]'
    _amount_input_form_label = 'xpath=.//*[@data-crlat="amountInputFormLabel"]'
    _enter_amount_label = 'xpath=.//*[@data-crlat="label.amount"]'
    _input_container = 'xpath=.//*[@data-crlat="value" or @data-crlat="enterAmount" or @data-crlat="inputContainer"]'  # TODO VOL-1036
    _amount_input_type = DepositInputBase
    _add_amount_label = 'xpath=.//*[@data-crlat="addAmount.label"]'
    _currency_input = 'xpath=.//*[@data-crlat="currency"]'  # TODO VOL-1036
    _deposit_button = 'xpath=.//*[@data-crlat="inputContainer"]'

    @property
    def input_currency_symbol(self):
        return self.before_element(selector=self._currency_input).replace('"', "")

    @property
    def enter_amount_label(self):
        return self._get_webelement_text(selector=self._enter_amount_label, timeout=1)

    @property
    def currency(self):
        return self._get_webelement_text(selector=self._amount_currency_label, timeout=3)

    @property
    def quick_amount_section(self):
        return self._quick_amount_section_type(selector=self._quick_amount_section, context=self._we)

    def get_quick_amount_labels(self):
        buttons = self.quick_amount_section.items_as_ordered_dict
        button_names = buttons.keys()
        return list(button_names)

    def click_quick_amount_button(self, amount):
        buttons = self.quick_amount_section.items_as_ordered_dict
        pattern = f'^.*{amount}$'
        input_value = self.input.value

        button = next((button for button_name, button in buttons.items() if re.match(pattern, button_name)), None)
        if not button:
            raise VoltronException(f'Quick amount button labeled "{amount}" not found in [{buttons.keys()}]')
        button.scroll_to_we()
        button.click()
        wait_for_result(lambda: input_value != self.input.value,
                        timeout=3,
                        name='Amount input value to change')

    def click_outside_amount_field(self):
        self.input.send_keys(Keys.SHIFT + Keys.TAB)

    @property
    def deposit_amount_field(self):
        return ButtonBase(selector=self._deposit_button, context=self._we)

    @property
    def input(self):
        return self._amount_input_type(selector=self._amount, context=self._we)

    # TODO VOL-1058
    @property
    def add_amount_label(self):
        return self._get_webelement_text(selector=self._add_amount_label, timeout=1)


class DepositAmountFormOnBetslip(DepositAmountForm):

    @property
    def _amount_input_type(self):
        device_type = get_device_properties()['type']
        if device_type in ['mobile', 'tablet', 'desktop']:
            return DepositInputBase
        return KeyboardInputBase
