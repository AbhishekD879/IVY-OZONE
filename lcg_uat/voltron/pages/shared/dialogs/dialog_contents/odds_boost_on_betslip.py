from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.pages.shared.dialogs.dialog_base import Dialog
from voltron.utils.waiters import wait_for_result


class OddsBoostOnBetslip(Dialog):
    _default_action = 'click_ok'
    _ok_button = 'xpath=.//*[@data-crlat="button.Ok"]'
    _thanks_link = 'xpath=.//*[@class="thanks"]'
    _dialog_content = 'xpath=.//*[@data-crlat="popUpText"]'
    _more_link = 'xpath=.//*[@data-crlat="button.More"]'

    @property
    def more_button(self):
        return ButtonBase(selector=self._more_link, context=self._we)

    def has_more_button(self, timeout=1, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._more_link,
                                                   timeout=0) is not None,
            name=f'Button status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)

    @property
    def description(self):
        return self._get_webelement_text(selector=self._dialog_content, context=self._we)

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
