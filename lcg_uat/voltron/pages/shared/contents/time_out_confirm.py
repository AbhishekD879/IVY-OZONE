from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.pages.shared.components.primitives.inputs import PasswordInput
from voltron.pages.shared.contents.base_content import BaseContent


class TimeOutPasswordConfirm(BaseContent):
    _url_pattern = r'^http[s]?:\/\/.+\/time-out/password-confirm'
    _password = 'xpath=.//*[@data-crlat="passwordConfirmInput"]'
    _continue_button = 'xpath=.//*[@data-crlat="continueButton"]'
    _cancel_button = 'xpath=.//*[@data-crlat="cancelButton"]'
    _confirm_title = 'xpath=.//*[@data-crlat="passwordConfirmTitle"]'
    _show_password = 'xpath=.//*[@data-crlat="showPasswordButton"]'
    _password_error = 'xpath=.//*[@data-crlat="passwordError"]'

    @property
    def password(self):
        return PasswordInput(selector=self._password)

    @property
    def continue_button(self):
        return ButtonBase(selector=self._continue_button)

    @property
    def cancel_button(self):
        return ButtonBase(selector=self._cancel_button)

    @property
    def confirm_title(self):
        return self._get_webelement_text(selector=self._confirm_title)

    @property
    def show_password(self):
        return ButtonBase(selector=self._show_password)

    @property
    def password_error(self):
        return self._get_webelement_text(selector=self._password_error)
