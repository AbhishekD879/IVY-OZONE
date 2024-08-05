from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.pages.shared.dialogs.dialog_base import Dialog


class AccountClosedDialog(Dialog):
    _ok_button = 'xpath=.//*[@data-crlat="button.ok"]'

    @property
    def ok_button(self):
        return ButtonBase(selector=self._ok_button)
