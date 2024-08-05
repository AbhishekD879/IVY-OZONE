from voltron.pages.shared.dialogs.dialog_base import Dialog
from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.utils.waiters import wait_for_result


class QuickDeposit(Dialog):
    _text = 'xpath=.//*[@data-crlat="text"]'
    _deposit_button = 'xpath=.//*[@data-uat="popUpText"]'
    _deposit_now_button = 'xpath=.//*[@data-uat="popUpButton"]'

    @property
    def text(self):
        return self._get_webelement_text(selector=self._text)

    def has_deposit_now_button(self, timeout=1, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._deposit_button,
                                                   timeout=0) is not None,
            name=f'Icon status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)

    @property
    def deposit_now_button(self):
        return ButtonBase(selector=self._deposit_now_button, context=self._we)
