from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.pages.shared.components.primitives.checkboxes import CheckBoxBase
from voltron.pages.shared.components.primitives.selects import SelectBase
from voltron.pages.shared.contents.base_content import BaseContent


class TimeOut(BaseContent):
    _url_pattern = r'^http[s]?:\/\/.+\/time-out'
    _timeout_select = 'xpath=.//*[@data-crlat="timeoutSelect"]'
    _continue_button = 'xpath=.//*[@data-crlat="continueButton"]'
    _cancel_button = 'xpath=.//*[@data-crlat="cancelButton"]'
    _reason_timeout = 'xpath=.//*[@data-crlat="reasonTimeout"]'

    @property
    def select_timeout(self):
        return SelectBase(selector=self._timeout_select)

    @property
    def continue_button(self):
        return ButtonBase(selector=self._continue_button)

    @property
    def cancel_button(self):
        return ButtonBase(selector=self._cancel_button)

    @property
    def reason_timeout(self):
        return ReasonForTimeout(selector=self._reason_timeout)


class ReasonRow(ComponentBase):
    _reason_checkbox = 'xpath=.//*[@data-crlat="reasonCheckbox"]'
    _reason_label = 'xpath=.//*[@data-crlat="checkboxLabel"]'

    @property
    def reason_checkbox(self):
        return CheckBoxBase(selector=self._reason_checkbox, context=self._we)

    @property
    def name(self):
        return self._get_webelement_text(selector=self._reason_label)


class ReasonForTimeout(ComponentBase):
    _item = 'xpath=.//*[@data-crlat="reasonRow"]'
    _list_item_type = ReasonRow
