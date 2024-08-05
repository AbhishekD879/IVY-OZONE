from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.pages.shared.dialogs.dialog_base import Dialog
from voltron.utils.waiters import wait_for_result


class RacingWatchFreeInfo(Dialog):
    _text = 'xpath=.//*[@data-crlat="textSection"]'
    _ok_button = 'xpath=.//*[@data-uat="popUpButton"]'
    _watch_free_logo = 'xpath=.//*[@data-crlat="wFLogo"]'
    _default_action = 'click_ok'

    @property
    def text(self):
        return self._get_webelement_text(selector=self._text)

    def click_ok(self):
        self.ok_button.click()

    def has_ok_button(self, timeout=1, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._ok_button,
                                                   timeout=0) is not None,
            name=f'Button status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)

    @property
    def ok_button(self):
        return ButtonBase(selector=self._ok_button, context=self._we)

    def has_watch_free_logo(self, timeout=1, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._watch_free_logo,
                                                   timeout=0) is not None,
            name=f'Button status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)

    def default_action(self):
        self.click_ok()
