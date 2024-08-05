from selenium.common.exceptions import InvalidElementStateException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys

from voltron.pages.shared import get_device_properties
from voltron.pages.shared import get_driver
from voltron.pages.shared.components.primitives.inputs import InputBase
from voltron.pages.shared.contents.registration.primitives.input import RegistrationInput
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.js_functions import click
from voltron.utils.js_functions import get_value
from voltron.utils.js_functions import mouse_event_click as safari_click
from voltron.utils.js_functions import scroll_into_view_above
from voltron.utils.waiters import wait_for_result


class GVCDepositInputBase(InputBase):

    @property
    def value(self):
        return wait_for_result(lambda: get_value(self._we),
                               timeout=0.6,
                               name='Value to appear')

    @value.setter
    def value(self, value):
        try:
            self._we.clear()
            self._we.send_keys(str(value))
        except InvalidElementStateException:
            self._we.send_keys(str(value))
        self._logger.debug(f'*** User has set "{value}" on Input. Call of "{self.__class__.__name__}"')
        self._we.send_keys(Keys.SHIFT + Keys.TAB)
        wait_for_result(lambda: str(self.value) == str(value),
                        timeout=0.5,
                        name='Set expected value')

    def perform_click(self, we=None):
        self._logger.debug(
            f'*** User has clicked "{self._we.text}" button. Call "{self.__class__.__name__}.click" method'
        )
        we = we if we else self._we
        if self.is_safari:
            get_driver().implicitly_wait(0.7)
            safari_click(we)
            get_driver().implicitly_wait(0)
        else:
            click(we)

    def send_keys(self, *args, **kwargs):
        super().send_keys(*args, **kwargs)
        self._we.send_keys(Keys.SHIFT + Keys.TAB)


class GVCDepositInput(RegistrationInput):
    _input_type = GVCDepositInputBase
    _is_focused_flag = 'md-input-focused'

    def is_valid_with_green_tick(self, expected_result=True, timeout=3):
        return wait_for_result(lambda: 'valid' in self.input.get_attribute('class'),
                               name='"Green tick" to appear',
                               expected_result=expected_result,
                               timeout=timeout)

    def click(self):
        device = get_device_properties()
        if device['type'] == 'desktop':
            scroll_into_view_above(self._we)
        try:
            self.input.perform_click()
        except WebDriverException as e:
            raise VoltronException(f'Can not click on {self.__class__.__name__}. {e}')
