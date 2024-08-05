from voltron.pages.shared.dialogs.dialog_base import Dialog
from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.utils.waiters import wait_for_result


class Error(Dialog):
    _message = 'xpath=.//*[@class="modal-body"]'
    _title = 'xpath=.//*[@class="container-header"]'
    _description = 'xpath=//*[@class="container-content"]'
    _ok_button = 'xpath=//*[@class="btn btn-style2" or @class="btn btn-style1 full-width"]'

    @property
    def title(self):
        return self._get_webelement_text(selector=self._title)

    @property
    def description(self):
        return self._get_webelement_text(selector=self._description)

    @property
    def ok_button(self):
        return ButtonBase(selector=self._ok_button, context=self._we)

    @property
    def message(self):
        return self._get_webelement_text(selector=self._message, timeout=0.5)
