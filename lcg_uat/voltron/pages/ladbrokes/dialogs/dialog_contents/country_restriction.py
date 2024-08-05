from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.pages.shared.dialogs.dialog_base import Dialog


class CountryRestriction(Dialog):
    _ok_button = 'xpath=.//button[text()="OK"]'
    _dialog_text = 'xpath=.//*[@class="modal-body"]/div[1]'

    @property
    def ok_button(self):
        return ButtonBase(selector=self._ok_button, timeout=1, context=self._we)

    @property
    def text(self):
        return self._get_webelement_text(selector=self._dialog_text, context=self._we)
