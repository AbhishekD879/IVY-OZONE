from voltron.pages.shared.dialogs.dialog_base import Dialog
from voltron.pages.shared.components.primitives.buttons import ButtonBase


class WatchLiveDialog(Dialog):
    _ok_button = 'xpath=.//*[@data-crlat="verifyMeButton"]'
    _error_msg = 'xpath=.//*[@data-crlat="errorMsg"]'

    @property
    def ok_button(self):
        return ButtonBase(selector=self._ok_button, timeout=1, context=self._we)

    @property
    def error_message(self):
        return self._get_webelement_text(selector=self._error_msg, context=self._we)
