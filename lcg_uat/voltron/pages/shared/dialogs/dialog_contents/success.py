from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.pages.shared.components.primitives.text_labels import TextBase
from voltron.pages.shared.dialogs.dialog_base import Dialog


class Success(Dialog):
    _message = 'xpath=.//*[@class="modal-body"]'
    _ok_button = 'xpath=//button[text()="OK"]'

    @property
    def message(self):
        return TextBase(selector=self._message, context=self._we).name

    @property
    def ok_button(self):
        return ButtonBase(selector=self._ok_button, timeout=1, context=self._we)
