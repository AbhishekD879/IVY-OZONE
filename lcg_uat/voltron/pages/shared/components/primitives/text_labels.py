from selenium.common.exceptions import ElementNotVisibleException

from voltron.pages.shared.components.base import ComponentBase
from voltron.utils.js_functions import click
from voltron.utils.waiters import wait_for_result


class TextBase(ComponentBase):
    _label = 'xpath=.//*[@data-crlat="label"] | .//label'
    _value = 'xpath=.//*[@data-crlat="value"] | .//div[@id="deposit-info"]'

    @property
    def text(self):
        return self._get_webelement_text(we=self._we)

    @property
    def name(self):
        return self._get_webelement_text(we=self._we)

    @property
    def label(self):
        return self._wait_for_not_empty_web_element_text(selector=self._label, timeout=1).strip()

    @property
    def value(self):
        return self._wait_for_not_empty_web_element_text(selector=self._value, timeout=1).strip()

    @property
    def is_bold(self):
        return self.css_property_value('font-weight') == '700'

    def click(self):
        self.scroll_to_we()
        try:
            self.perform_click()
        except ElementNotVisibleException as e:
            self._logger.warning(f'**** Bypassing exception {e}')
            click(self._we)


class LinkBase(TextBase):

    def get_link(self):
        result = wait_for_result(lambda: self.get_attribute('href'),
                                 name=f'{self.__class__.__name__} href attribute is not empty',
                                 timeout=1)
        return result
