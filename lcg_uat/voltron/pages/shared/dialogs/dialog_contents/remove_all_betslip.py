from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.pages.shared.dialogs.dialog_base import Dialog
from voltron.utils.waiters import wait_for_result


class RemoveAllBetslip(Dialog):
    _continue_button = 'xpath=.//*[@data-crlat="button.Continue"]'
    _cancel_button = 'xpath=.//*[@data-crlat="button.Cancel"]'
    _text = 'xpath=.//*[@data-crlat="popUpText"]'
    _default_action = 'click_continue'

    @property
    def continue_button(self):
        return ButtonBase(selector=self._continue_button, context=self._we)

    def has_continue_button(self, expected_result=True, timeout=3):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._continue_button, timeout=0) is not None,
                               name=f'"Continue" button shown status to be "{expected_result}"',
                               expected_result=expected_result,
                               timeout=timeout)

    @property
    def cancel_button(self):
        return ButtonBase(selector=self._cancel_button, context=self._we)

    def has_cancel_button(self, expected_result=True, timeout=3):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._cancel_button, timeout=0) is not None,
                               name=f'"Cancel" button shown status to be "{expected_result}"',
                               expected_result=expected_result,
                               timeout=timeout)

    @property
    def text(self):
        return self._get_webelement_text(selector=self._text)

    def click_continue(self):
        self.continue_button.click()

    def default_action(self):
        self.click_continue()
