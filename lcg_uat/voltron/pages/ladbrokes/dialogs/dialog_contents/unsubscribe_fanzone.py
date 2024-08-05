from voltron.pages.shared.dialogs.dialog_base import Dialog
from voltron.pages.shared.components.primitives.buttons import ButtonBase


class UnsubscribeFanzone(Dialog):
    _title = 'xpath=.//*[contains(@class, "notification-title")]'
    _description = 'xpath=.//*[contains(@class, "notification-text")]'
    _exit_button = 'xpath=.//*[@class="footer-btn exit"]'
    _confirm_button = 'xpath=.//*[contains(@class, "footer-btn confirm")]'

    @property
    def title(self):
        return self._get_webelement_text(selector=self._title, timeout=5)

    @property
    def description(self):
        return self._get_webelement_text(selector=self._description, timeout=5)

    @property
    def exit_button(self):
        return ButtonBase(selector=self._exit_button, timeout=5)

    @property
    def confirm_button(self):
        return ButtonBase(selector=self._confirm_button, timeout=5)
