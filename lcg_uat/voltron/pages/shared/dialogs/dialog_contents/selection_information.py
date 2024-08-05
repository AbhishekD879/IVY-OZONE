from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.pages.shared.dialogs.dialog_base import Dialog


class SelectionInformation(Dialog):
    _ok_button = 'xpath=.//*[@data-crlat="button.OK"]'

    @property
    def ok_button(self):
        return ButtonBase(selector=self._ok_button)

    def click_ok(self):
        self.ok_button.click()

    @property
    def text(self):
        return self._get_webelement_text(selector=self._dialog_content, context=self._we)
