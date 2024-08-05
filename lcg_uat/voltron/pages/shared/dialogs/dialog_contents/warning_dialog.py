from voltron.pages.shared.dialogs.dialog_base import Dialog
from voltron.pages.shared.components.primitives.buttons import ButtonBase


class WarningDialog(Dialog):
    _dialog_text = 'xpath=.//*[@data-crlat="proceedLuckyDipText"]'
    _accept_button = 'xpath=.//*[@data-crlat="acceptButton"]'
    _cancel_button = 'xpath=.//*[@data-crlat="cancelButton"]'

    @property
    def text(self):
        return self._get_webelement_text(selector=self._dialog_text, context=self._we)

    @property
    def accept_button(self):
        return ButtonBase(selector=self._accept_button, context=self._we)

    @property
    def cancel_button(self):
        return ButtonBase(selector=self._cancel_button, context=self._we)
