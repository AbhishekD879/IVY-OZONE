from voltron.pages.shared.components.keyboard.mobile_keyboard import Keyboard
from voltron.pages.shared.components.primitives.inputs import InputBase
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.js_functions import get_value
from voltron.utils.waiters import wait_for_result


class KeyboardInputBase(InputBase):
    _keyboard = 'xpath=//*[@data-crlat="betslip.keyboard"]'
    _send_keys_delay = 0.1

    @property
    def value(self):
        return get_value(self._we)

    def clear(self):
        self._we.click()
        self._wait_for_mobile_keyboard()
        [self._ui_keyboard.enter_amount_using_keyboard(value='delete') for _ in str(self.value)]
        self._ui_keyboard.enter_amount_using_keyboard(value='enter')

    @value.setter
    def value(self, value):
        self._we.click()
        self._wait_for_mobile_keyboard()
        self._ui_keyboard.enter_amount_using_keyboard(value=value)
        self._logger.debug(
            f'*** User has set "{value}" on Input. Call of "{self.__class__.__name__}"'
        )
        self._ui_keyboard.enter_amount_using_keyboard(value='enter')

    def send_keys(self, keys, delay=_send_keys_delay):
        self.value = keys

    @property
    def _ui_keyboard(self):
        return Keyboard(selector=self._keyboard, context=self._we, timeout=2)

    def _wait_for_mobile_keyboard(self):
        result = wait_for_result(lambda: self._find_element_by_selector(selector=self._keyboard,
                                                                        timeout=0) and self._find_element_by_selector(selector=self._keyboard,
                                                                                                                      timeout=0).is_displayed(),
                                 name='Mobile UI keyboard to show',
                                 timeout=2)
        if not result:
            raise VoltronException('Mobile UI keyboard was not found')

    def scroll_to_we(self, web_element=None):
        """
        Bypassing scroll as element in a view
        """
        pass
