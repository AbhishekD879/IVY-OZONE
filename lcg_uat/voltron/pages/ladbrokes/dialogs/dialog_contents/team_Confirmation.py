from voltron.pages.shared.dialogs.dialog_base import Dialog
from voltron.pages.shared.components.primitives.buttons import ButtonBase


class TeamConfirmation(Dialog):
    _description = 'xpath=.//*[@class="SYC-Popup-text"]'
    _select_different_button = 'xpath=.//button[contains(@class, "SYC-Popup__ctaButton--ctaPrimaryBtn")]'
    _confirm_button = 'xpath=.//*[contains(@class, "SYC-Popup__ctaButton--ctaSecondaryBtn")]'
    _card_img = 'xpath=.//*[@class="SYC-Popup-img"]'
    _card_dialog_text = 'xpath=.//*[contains(@class, "card-dialog-text")]'

    @property
    def description(self):
        return self._get_webelement_text(selector=self._description, timeout=5)

    @property
    def card_dialog_text(self):
        return self._get_webelement_text(selector=self._card_dialog_text, timeout=5)

    @property
    def select_different_button(self):
        return ButtonBase(selector=self._select_different_button, timeout=5)

    @property
    def exit_button(self):
        return ButtonBase(selector=self._confirm_button, timeout=5)

    @property
    def confirm_button(self):
        return ButtonBase(selector=self._confirm_button, timeout=5)

    @property
    def card_img(self):
        return self._get_webelement_text(selector=self._card_img, timeout=5)

    @property
    def team_confirmation_exit_button(self):
        return ButtonBase(selector=self._select_different_button, timeout=5)
