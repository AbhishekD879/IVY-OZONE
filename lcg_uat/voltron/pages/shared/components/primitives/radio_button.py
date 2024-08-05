from voltron.pages.shared import get_driver
from voltron.pages.shared.components.base import ComponentBase
from voltron.utils.waiters import wait_for_result


class RadioButtonBase(ComponentBase):
    _label = 'xpath=.//*[@data-crlat="label"]'
    _select_button = 'xpath=.//*[@data-crlat="input"]'

    @property
    def label(self):
        return self._find_element_by_selector(selector=self._label)

    @property
    def name(self):
        return self._get_webelement_text(selector=self._label)

    @property
    def select(self):
        return self._find_element_by_selector(selector=self._select_button)

    @select.setter
    def select(self, value):
        value = bool(value)
        if self.is_checked() != value:
            drv = get_driver()
            drv.execute_script("return arguments[0].click();", self.select)
            self._logger.debug(
                f'*** User has set "{value}" on RadioButton. Call of "{self.__class__.__name__}"'
            )
            wait_for_result(lambda: self.is_checked() == value,
                            timeout=3)
        else:
            self._logger.warning('*** Bypassing click on radio button as its status already: %s' % value)

    def is_checked(self, timeout=1, expected_result=True):
        return wait_for_result(lambda: 'ng-valid-parse' in self.select.get_attribute('class').strip(' ').split(' '),
                               timeout=timeout,
                               name='Select radio button checked status to be %s' % expected_result,
                               expected_result=expected_result)
