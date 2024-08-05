from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException

from voltron.pages.shared import get_device_properties
from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.primitives.inputs import InputBase
from voltron.pages.shared.components.primitives.keyboard_input import KeyboardInputBase
from voltron.utils.waiters import wait_for_result


class AmountForm(ComponentBase):
    _amount = 'xpath=.//*[@data-crlat="value"]'
    _amount_input_form_label = 'xpath=.//*[@data-crlat="label"]'
    _amount_currency_label = 'xpath=.//label[@data-currency] | .//*[@data-crlat="currencySymbol"]'
    _error_message = 'xpath=.//*[@data-crlat="minDepositAmount"]'

    @property
    def error_message(self):
        self.scroll_to_we()
        return wait_for_result(lambda: self._get_webelement_text(selector=self._error_message),
                               name='Error message to appear',
                               timeout=2)

    @property
    def _amount_input_type(self):
        device_type = get_device_properties()['type']
        if device_type in ['mobile', 'tablet', 'desktop']:
            return InputBase
        return KeyboardInputBase

    def enter_amount(self, value=''):
        if not isinstance(value, str):
            value = str(value)
        self.input.value = value

    @property
    def label(self):
        return self._get_webelement_text(selector=self._amount_input_form_label, context=self._we)

    @property
    def input(self):
        return self._amount_input_type(selector=self._amount, context=self._we)

    def has_amount_input(self, expected_result=True, timeout=1):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._amount, timeout=0) is not None,
                               expected_result=expected_result,
                               timeout=timeout,
                               name=f'Amount input presence status to be "{expected_result}"')

    @property
    def default_value(self):
        return ComponentBase(selector=self._amount, context=self._we).get_attribute('placeholder')

    @property
    def currency(self):
        return ComponentBase(selector=self._amount_currency_label, context=self._we).get_attribute('data-currency')

    @property
    def is_alternative_amount_shown(self):
        return 'offered' in self.get_attribute('class')

    @property
    def input_container(self):
        return self.input  # to handle inheritance on DepositAmountForm

    def is_active(self, expected_result=True, timeout=1, poll_interval=0.5, name=None,
                  bypass_exceptions=(NoSuchElementException, StaleElementReferenceException, TypeError)):
        if not name:
            name = '"%s" enabled status is: %s' % (self.__class__.__name__, expected_result)
        result = wait_for_result(lambda: 'dk-active-input' in self.input_container.get_attribute('class'),
                                 expected_result=expected_result,
                                 timeout=timeout,
                                 poll_interval=poll_interval,
                                 name=name,
                                 bypass_exceptions=bypass_exceptions)
        return result
