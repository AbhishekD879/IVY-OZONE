from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.pages.shared.components.primitives.checkboxes import ConfirmCheckBox
from voltron.pages.shared.dialogs.dialog_base import Dialog


class ConfirmationOfTimeOut(Dialog):
    _cancel_button = 'xpath=.//*[@data-crlat="dialogCancel"]'
    _yes_button = 'xpath=.//*[@data-crlat="dialogYes"]'
    _confirm_checkbox = 'xpath=.//*[@data-crlat="confirmCheckbox"]'
    _deposit_limit_link = 'xpath=.//*[@data-crlat="depositLimitLink"]'
    _game_play_link = 'xpath=.//*[@data-crlat="gamePlayReminderLink"]'
    _unlock_date_text = 'xpath=.//*[@data-crlat="unlockDate"]'
    _default_action = 'click_yes'

    @property
    def yes_button(self):
        return ButtonBase(selector=self._yes_button, context=self._we)

    @property
    def cancel_button(self):
        return ButtonBase(selector=self._cancel_button, context=self._we)

    @property
    def confirm_checkbox(self):
        return ConfirmCheckBox(selector=self._confirm_checkbox, context=self._we)

    @property
    def deposit_limit_link(self):
        return ButtonBase(selector=self._deposit_limit_link, context=self._we)

    @property
    def game_play_link(self):
        return ButtonBase(selector=self._game_play_link, context=self._we)

    @property
    def unlock_date_text(self):
        return self._get_webelement_text(selector=self._unlock_date_text, context=self._we)

    def click_yes(self):
        self.yes_button.click()

    def default_action(self):
        self.click_yes()
