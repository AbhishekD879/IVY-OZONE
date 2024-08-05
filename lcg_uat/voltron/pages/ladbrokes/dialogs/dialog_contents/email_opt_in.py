from voltron.pages.shared.dialogs.dialog_base import Dialog
from voltron.pages.shared.components.primitives.buttons import ButtonBase


class EmailOptIn(Dialog):
    _do_not_show_me_again = 'xpath=.//*[@class="dont-show-me"]'
    _option_mail_popup_title = 'xpath=.//*[@class="optinEmail-Popup-title"]'
    _option_mail_popup_text = 'xpath=.//*[@class="optinEmail-Popup-text"]'
    _remind_me_later = 'xpath=.//*[@class="remind-later"]'
    _option_mail_button = 'xpath=.//*[@class="optin-email-button"]'

    @property
    def do_not_show_me_again(self):
        return ButtonBase(selector=self._do_not_show_me_again, timeout=2)

    @property
    def option_mail_popup_title(self):
        return self._get_webelement_text(selector=self._option_mail_popup_title)

    @property
    def option_mail_popup_text(self):
        return self._get_webelement_text(selector=self._option_mail_popup_text)

    @property
    def remind_me_later(self):
        return ButtonBase(selector=self._remind_me_later, timeout=2)

    @property
    def option_mail_button(self):
        return ButtonBase(selector=self._option_mail_button, timeout=2)
