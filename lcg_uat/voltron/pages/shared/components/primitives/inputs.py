from time import sleep

from selenium.common.exceptions import InvalidElementStateException, ElementNotInteractableException
from selenium.webdriver.common.keys import Keys

import tests
from voltron.pages.shared import get_driver
from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.utils.helpers import find_element
from voltron.utils.helpers import parse_pattern
from voltron.utils.js_functions import get_value
from voltron.utils.js_functions import set_value
from voltron.utils.waiters import wait_for_result


class InputBase(ComponentBase):

    _send_keys_delay = 0.1

    @property
    def value(self):
        self.scroll_to_we()
        value = wait_for_result(lambda: get_value(self._we),
                                timeout=0.6,
                                name='Value to appear')
        return value

    @value.setter
    def value(self, value):
        self.scroll_to_we()
        driver = get_driver()
        try:
            self._we.clear()
            self.send_keys(str(value))
        except (InvalidElementStateException, ElementNotInteractableException):
            driver.execute_script("arguments[0].value='';arguments[0]", self._we)
            driver.execute_script(f"arguments[0].value={value};arguments[0].dispatchEvent(new Event('change'));",
                                  self._we)
        self._logger.debug(
            f'*** User has set "{value}" on Input. Call of "{self.__class__.__name__}"'
        )
        try:
            self._we.send_keys(Keys.SHIFT + Keys.TAB)
        except (InvalidElementStateException, ElementNotInteractableException):
            pass
        wait_for_result(lambda: str(self.value) == str(value),
                        timeout=1,
                        name=f'{self.__class__.__name__} value to appear')
        # try:
        #     if tests.settings.device_type == 'mobile' and tests.use_browser_stack:
        #         get_driver().hide_keyboard()
        # except Exception as e:
        #     self._logger.warning(f'*** Unable to hide keyboard: {e}')

    @property
    def placeholder(self):
        return self.get_attribute('placeholder')

    def clear(self):
        set_value(self._we, '')
        value = get_value(self._we)
        if value:
            self._we.clear()

    def send_keys(self, keys, delay=_send_keys_delay):
        for symbol in str(keys):
            self._we.send_keys(symbol)
            sleep(delay)

    def is_active(self, expected_result=True, timeout=1):
        return wait_for_result(lambda: self._we.is_displayed() and self._we.is_enabled(),
                               expected_result=expected_result,
                               timeout=timeout,
                               name=f'Amount input active status to be "{expected_result}"')


class RegistrationInput(InputBase):
    _error = 'xpath=.//*[@data-crlat="errorMessage.{dataCrlat}"]'
    _pattern_values = {}
    _passport_error = 'xpath=.//*[@data-crlat="signposting"]'

    def _wait_active(self, timeout=0):
        self._we = self._find_myself()
        wait_for_result(lambda: self._we.is_enabled(),
                        name=f'"{self.__class__.__name__}" to be enabled',
                        timeout=15)

    @property
    def error(self):
        selector = parse_pattern(pattern_data=self._error, pattern_values=self._pattern_values)
        we = find_element(selector=selector, timeout=4)
        error_text = self._get_webelement_text(we=we) if we else ''
        return error_text

    @property
    def error_passport(self):
        selector = parse_pattern(pattern_data=self._passport_error, pattern_values=self._pattern_values)
        we = find_element(selector=selector, timeout=4)
        error_text = self._get_webelement_text(we=we) if we else ''
        return error_text

    def get_label(self):
        return self.placeholder

    def get_value(self):
        return self.value

    def set_value(self, data):
        self.value = data

    @property
    def value(self):
        self.scroll_to_we()
        return self.get_attribute('value')

    @value.setter
    def value(self, value):
        self.scroll_to_we()
        self._we.clear()
        self._we.send_keys(value)
        self._logger.debug(
            f'*** User has set "{value}" on RegistrationInput. Call of "{self.__class__.__name__}"'
        )
        self._we.send_keys(Keys.SHIFT + Keys.TAB)


class PasswordInput(InputBase):
    _show_button = 'xpath=.//*[contains(@class, "theme-hide-password")]'
    _hide_button = 'xpath=.//*[contains(@class, "theme-show-password")]'

    @property
    def show_button(self):
        return ButtonBase(selector=self._show_button)

    @property
    def hide_button(self):
        return ButtonBase(selector=self._hide_button)

    @property
    def input_type(self):
        return self.get_attribute('type')

    @property
    def input_value(self):
        return self.get_attribute('value')
