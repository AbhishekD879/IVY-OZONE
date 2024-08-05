from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException

from voltron.pages.shared.components.base import ComponentBase
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.helpers import find_element
from voltron.utils.helpers import parse_pattern
from voltron.utils.js_functions import click
from voltron.utils.waiters import wait_for_result


class CheckBoxBase(ComponentBase):
    _input = 'xpath=.//input'

    @property
    def value(self):
        self.scroll_to_we()
        we = self._find_element_by_selector(selector=self._input)
        if we:
            value = we.is_selected()
        else:
            raise VoltronException('Cannot get checkbox value')
        if value:
            return True
        return False

    @value.setter
    def value(self, value):
        if not isinstance(value, bool):
            raise VoltronException('CheckBox value should be BOOL type (True/False). Got: "%s"' % value)

        if self.value != value:
            if self.is_enabled():
                self._logger.debug(
                    f'*** User has set "{value}" on CheckBox. Call of "{self.__class__.__name__}"'
                )
                self.click()
            else:
                raise VoltronException('CheckBox is disabled so can\'t be clicked')


class BuildYourRacecardCheckBox(CheckBoxBase):

    def is_enabled(self, expected_result=True, timeout=1, poll_interval=0.5, name=None,
                   bypass_exceptions=(NoSuchElementException, StaleElementReferenceException, TypeError)) -> bool:
        if not name:
            name = f'"{self.__class__.__name__}" enabled status is: {expected_result}'
        we = self._find_element_by_selector(self._input)
        result = wait_for_result(lambda: we.is_enabled(),
                                 expected_result=expected_result,
                                 timeout=timeout,
                                 poll_interval=poll_interval,
                                 name=name,
                                 bypass_exceptions=bypass_exceptions)
        return result


class RegistrationCheckBox(CheckBoxBase):
    _text = 'xpath=.//*[@data-crlat="text"]'
    _error = 'xpath=.//*[@data-crlat="errorMessage.{dataCrlat}"]'
    _input = 'xpath=.//*[@data-crlat="input"]'
    _check_box = 'xpath=.//*[@data-crlat="checkBox"]'
    _pattern_values = {}

    @property
    def text(self):
        return self._get_webelement_text(selector=self._text, timeout=2)

    @property
    def error(self):
        selector = parse_pattern(pattern_data=self._error, pattern_values=self._pattern_values)
        we = find_element(selector=selector, timeout=2)
        error_message_text = self._get_webelement_text(we=we) if we else ''
        return error_message_text

    @property
    def value(self):
        self.scroll_to_we()
        input_ = self._find_element_by_selector(selector=self._input, timeout=2)
        value = 'true' in input_.get_attribute('value')
        return value

    @value.setter
    def value(self, value):
        if not isinstance(value, bool):
            raise VoltronException('CheckBox value should be BOOL type (True/false). Got: "%s"' % value)

        if self.value != value:
            check_box = self._find_element_by_selector(self._input, timeout=2)
            self._logger.debug(
                f'*** User has set "{value}" on CheckBox. Call of "{self.__class__.__name__}"'
            )
            click(check_box)


class ConfirmCheckBox(CheckBoxBase):
    _input = 'xpath=.//input'

    def is_enabled(self, expected_result=True, timeout=1, poll_interval=0.5, name=None,
                   bypass_exceptions=(NoSuchElementException, StaleElementReferenceException, TypeError)) -> bool:
        if not name:
            name = '"%s" enabled status is: %s' % (self.__class__.__name__, expected_result)
        result = wait_for_result(lambda: self._we.is_enabled(),
                                 expected_result=expected_result,
                                 timeout=timeout,
                                 poll_interval=poll_interval,
                                 name=name,
                                 bypass_exceptions=bypass_exceptions)
        return result

    def click(self):
        we = self._find_element_by_selector(selector=self._input)
        if we:
            click(we)
        else:
            raise VoltronException('Cannot click on Confirm checkbox')
