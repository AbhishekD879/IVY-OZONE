from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.pages.shared.dialogs.dialog_base import Dialog
from voltron.utils.js_functions import click
from voltron.utils.waiters import wait_for_result


class AcceptDeclineButton(ButtonBase):

    def click(self, scroll_to=True):
        self.scroll_to_we() if scroll_to else None
        click(self._we)


class Congratulations(Dialog):
    _message = 'xpath=.//*[@class="modal-body"]'
    _bonus_message = 'xpath=.//*[@data-uat="popUpText"]'
    _decline_button = 'xpath=.//*[@data-crlat="dialog.decline"]'
    _accept_button = 'xpath=.//*[@data-crlat="dialog.accept"]'
    _close_button = 'xpath=.//*[@data-uat="popUpCloseButton"]'
    _ok_button = 'xpath=//button[text()="OK"]'
    _default_action = 'click_accept'

    @property
    def message(self):
        return self._get_webelement_text(selector=self._message, context=self._we)

    @property
    def bonus_message(self):
        return self.strip_currency_sign(self._get_webelement_text(selector=self._bonus_message, context=self._we))

    @property
    def decline_button(self):
        return AcceptDeclineButton(selector=self._decline_button, timeout=1, context=self._we)

    @property
    def accept_button(self):
        return AcceptDeclineButton(selector=self._accept_button, timeout=1, context=self._we)

    @property
    def close_button(self):
        return ButtonBase(selector=self._close_button, context=self._we, timeout=5)

    @property
    def ok_button(self):
        return ButtonBase(selector=self._ok_button, timeout=1, context=self._we)

    def has_accept_button(self, timeout=1, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._accept_button,
                                                   timeout=0) is not None,
            name=f'Button status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)

    def click_accept(self):
        if self.has_accept_button(timeout=5):
            self.accept_button.click()
        else:
            self.close_button.click()
