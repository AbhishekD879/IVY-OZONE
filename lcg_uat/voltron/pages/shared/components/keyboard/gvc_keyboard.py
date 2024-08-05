from time import sleep

from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import WebDriverException

from voltron.pages.shared.components.keyboard.mobile_keyboard import Key
from voltron.pages.shared.components.keyboard.mobile_keyboard import Keyboard
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.js_functions import natural_mouse_click
from voltron.utils.waiters import wait_for_result


class GVCKey(Key):

    @property
    def name(self):
        return self._get_webelement_text(we=self._we)

    @property
    def text(self):
        return self.name

    def click(self):
        self.scroll_to_we()
        try:
            self._logger.debug(
                f'*** User has clicked "{self._we.text}" button. Call "{self.__class__.__name__}.click" method'
            )
            natural_mouse_click(self._we)
        except WebDriverException as e:
            raise VoltronException(f'Can not click on {self.__class__.__name__}. {e}')

    def scroll_to_we(self, web_element=None):
        """
        No scroll should be executed on key
        """
        pass


class GVCKeyboard(Keyboard):
    _item = 'xpath=.//div[@ng-repeat="key in row"]//button'
    _list_item_type = GVCKey
    _keys = None

    def _wait_active(self, timeout=3):
        self._we = self._find_myself(timeout=timeout)
        wait_for_result(lambda: self._we.size.get('height') > 50 and self._we.size.get('width') > 50,
                        timeout=timeout,
                        name='Right menu to appear in expanded size')
        wait_for_result(lambda: len(self._find_elements_by_selector(selector=self._item, timeout=0)) > 1,
                        name='Keyboard to be loaded with keys',
                        timeout=timeout)

    @property
    def _special_keys(self):
        return {'delete': '⌫',
                'enter': '↵',
                '00': '00'
                }

    def enter_amount_using_keyboard(self, value='', delay=0.5):
        if not isinstance(value, (str,)):
            value = str(value)
        keys = self.keys
        if value in ('enter', 'delete', '00'):
            value = self._special_keys.get(value)
            keys[value].click()
            sleep(delay)
        else:
            for key_title in value:
                key = keys.get(key_title)
                if not key:
                    raise VoltronException(f'Key "{key_title}" not found in keys {list(keys.keys())}')
                try:
                    key.click()
                    sleep(delay)
                except (ElementNotVisibleException, VoltronException):
                    key.click()
                    sleep(delay)
                except KeyError:
                    raise VoltronException(f'No such key "{value}" found on keyboard')
