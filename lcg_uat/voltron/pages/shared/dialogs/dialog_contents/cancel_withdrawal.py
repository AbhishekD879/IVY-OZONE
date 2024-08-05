from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.pages.shared.dialogs.dialog_base import Dialog


class CancelWithdrawal(Dialog):
    _default_action = 'click_cancel_withdrawal'

    _cancel_withdrawal_button = 'xpath=.//*[@data-crlat="button.confirm"]'
    _close_button = 'xpath=.//*[@data-crlat="button.close"]'

    @property
    def cancel_withdrawal_button(self):
        return ButtonBase(selector=self._cancel_withdrawal_button, context=self._we)

    @property
    def close_button(self):
        return ButtonBase(selector=self._close_button, context=self._we)

    def click_cancel_withdrawal(self):
        self.cancel_withdrawal_button.click()
