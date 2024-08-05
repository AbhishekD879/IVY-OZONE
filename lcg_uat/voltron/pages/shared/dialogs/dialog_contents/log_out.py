from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.pages.shared.dialogs.dialog_base import Dialog
from voltron.utils.waiters import wait_for_result


class LoggedOut(Dialog):
    _error_title = 'xpath=.//*[@data-crlat="dialog.errorTitle"]'
    _text_message = 'xpath=.//*[@data-crlat="dialog.errorMessage"]'
    _customer_services_link = 'xpath=.//*[@data-crlat="dialog.link"]'
    _cancel_button = 'xpath=.//*[@data-crlat="dialog.cancel"]'
    _login_button = 'xpath=.//*[@data-crlat="dialog.login"]'

    _default_action = 'close_dialog'

    @property
    def error_title(self):
        return self._get_webelement_text(selector=self._error_title)

    @property
    def message(self):
        return self._get_webelement_text(selector=self._text_message)

    @property
    def customer_services(self):
        return ButtonBase(selector=self._customer_services_link)

    @property
    def cancel(self):
        return ButtonBase(selector=self._cancel_button)

    @property
    def has_cancel_button(self):
        return self._find_element_by_selector(selector=self._cancel_button, timeout=2) is not None

    @property
    def login(self):
        return ButtonBase(selector=self._login_button)

    def has_login_button(self, expected_result=True, timeout=2):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._login_button,
                                                                      timeout=0),
                               expected_result=expected_result,
                               timeout=timeout,
                               name=f'Login button status to be {expected_result}')
