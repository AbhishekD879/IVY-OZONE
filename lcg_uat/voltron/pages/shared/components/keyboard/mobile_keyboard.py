from time import sleep
from selenium.common.exceptions import ElementNotVisibleException
from voltron.pages.shared.components.base import ComponentBase
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.js_functions import click


class Key(ComponentBase):

    @property
    def name(self):
        return self.get_attribute('data-value')

    @property
    def text(self):
        return self._get_webelement_text(we=self._we)

    def click(self):
        self._logger.debug(
            f'*** User has clicked "{self._we.text}" button. Call "{self.__class__.__name__}.click" method'
        )
        click(self._we)

    def scroll_to_we(self, web_element=None):
        """
        Bypassing scroll as element in a view
        """
        pass


class Keyboard(ComponentBase):
    _item = 'xpath=.//*[@data-crlat="keyboard.key"]'
    _list_item_type = Key
    _keys = None

    @property
    def keys(self):
        if self._keys is None:
            self._keys = self.items_as_ordered_dict
        return self._keys

    def enter_amount_using_keyboard(self, value='', delay=1):
        if not isinstance(value, (str,)):
            value = str(value)
        keys = self.keys
        if value in ('enter', 'delete', '00'):
            keys[value].click()
            sleep(delay)
        elif value in 'free-bet':
            keys[value]._we.click()
        else:
            for key in value:
                try:
                    sleep(delay)
                    keys[key].click()
                    sleep(delay)
                except (ElementNotVisibleException, VoltronException):
                    keys[key].click()
                    sleep(delay)
                except KeyError:
                    raise VoltronException(f'No such key "{value}" found on keyboard')

    def scroll_to_we(self, web_element=None):
        """
        Bypassing scroll as element in a view
        """
        pass
