from voltron.pages.shared.dialogs.dialog_base import Dialog
from voltron.pages.shared.components.primitives.buttons import ButtonBase


class EditAccaCancelDialog(Dialog):
    _text = 'xpath=.//*[@data-crlat="dTitle"]'
    _description = 'xpath=//*[@data-crlat="popUpText"]'
    _cancel_edit_button = 'xpath=.//*[@data-crlat="button.Cancel edit"]'
    _continue_edit_button = _cancel_edit_button

    @property
    def text(self):
        return self._get_webelement_text(selector=self._text)

    @property
    def description(self):
        return self._get_webelement_text(selector=self._description)

    @property
    def cancel_edit_button(self):
        return ButtonBase(selector=self._cancel_edit_button, context=self._we)

    @ property
    def continue_edit_button(self):
        return ButtonBase(selector=self._continue_edit_button, context=self._we)
