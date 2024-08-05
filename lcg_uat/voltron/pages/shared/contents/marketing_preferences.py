from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.pages.shared.components.primitives.checkboxes import CheckBoxBase
from voltron.pages.shared.components.primitives.text_labels import TextBase
from voltron.pages.shared.components.base import ComponentBase
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.waiters import wait_for_result


class MarketingPreferencesCheckBox(CheckBoxBase):
    _label_checkboxes = 'xpath=.//*[@data-crlat="checkboxLabel"]'
    _input = 'xpath=.//*[@data-crlat="input"]'

    @property
    def label(self):
        return TextBase(selector=self._label_checkboxes, context=self._we, timeout=0.5)

    @property
    def name(self):
        return self._get_webelement_text(selector=self._label_checkboxes, context=self._we, timeout=0.5)

    def is_selected(self, expected_result=True, timeout=2, poll_interval=0.5, name=None) -> bool:
        input_ = self._find_element_by_selector(selector=self._input, context=self._we)
        if not name:
            name = f'"{self.__class__.__name__}" selected status is: {expected_result}'
        result = wait_for_result(lambda: input_.is_selected(),
                                 expected_result=expected_result,
                                 timeout=timeout,
                                 poll_interval=poll_interval,
                                 name=name,
                                 bypass_exceptions=(NoSuchElementException, StaleElementReferenceException, AttributeError))
        return result

    def click(self):
        if self.label:
            self.label.click()
        else:
            raise VoltronException(f'"{self.name}" button is disabled')


class MarketingPreferences(ComponentBase):
    _item = 'xpath=.//*[@data-crlat="checkboxGroup"]'
    _list_item_type = MarketingPreferencesCheckBox
    _title = 'xpath=.//*[@data-crlat="topBarTitle"]'
    _footer_text = 'xpath=.//*[@data-crlat="policyTextBlock"]'
    _info_text = 'xpath=.//*[@data-crlat="caption"]'
    _submit_button = 'xpath=.//*[@data-crlat="button.saveMyPreferences"]'
    _fade_out_overlay = True
    _verify_spinner = True

    @property
    def title(self):
        return self._get_webelement_text(selector=self._title)

    @property
    def caption(self):
        return self._get_webelement_text(selector=self._info_text)

    @property
    def submit_button(self):
        return ButtonBase(selector=self._submit_button, context=self._we)

    @property
    def footer_text(self):
        return self._get_webelement_text(selector=self._footer_text, timeout=2)
