from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.pages.shared.components.primitives.selects import SelectBase


class TimeManagementContainer(ComponentBase):
    _name = 'xpath=.//option'

    @property
    def name(self):
        return self._wait_for_not_empty_web_element_text(selector=self._name, context=self._we, timeout=1)


class TimeManagement(ComponentBase):
    _url_pattern = r'^http[s]?:\/\/.+\/realitycheckpreferences'
    _save_button = 'xpath=.//*[contains(text(), "Save")]'
    _values_dropdown = 'xpath=.//*[@name="gameTimeLimit"]'
    _list_item_type = TimeManagementContainer
    _dropdown = 'xpath=.//select'
    _dropdown_type = SelectBase
    _message = 'xpath=.//*[@class="cms-container"]'

    @property
    def successful_message(self):
        return self._find_element_by_selector(selector=self._message, context=self._we)

    @property
    def dropdown(self):
        return self._dropdown_type(selector=self._dropdown, context=self._we)

    @property
    def save_button(self):
        return ButtonBase(selector=self._save_button, context=self._we)

    @property
    def values_dropdown(self):
        return ButtonBase(selector=self._values_dropdown, context=self._we)
