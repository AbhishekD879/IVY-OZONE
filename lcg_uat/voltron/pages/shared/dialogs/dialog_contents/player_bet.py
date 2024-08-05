from voltron.pages.shared.dialogs.dialog_base import Dialog
from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.utils.waiters import wait_for_result


class PlayerBet(Dialog):
    _pop_up_title = 'xpath=.//*[@data-uat="popUpTitle"]'
    _pop_up_text = 'xpath=.//*[@data-crlat="popUpText"]'
    _ok_thanks_btn = 'xpath=.//*[@data-crlat="button.Ok, Thanks"]'

    @property
    def pop_up_text(self):
        return self._get_webelement_text(selector=self._pop_up_text)

    @property
    def pop_up_title(self):
        return self._get_webelement_text(selector=self._pop_up_title)

    @property
    def ok_thanks_btn(self):
        wait_for_result (
            lambda: self._find_elements_by_selector(selector=self._ok_thanks_btn, context=self._we) is not None,
            expected_result=True)
        return ButtonBase(selector=self._ok_thanks_btn, context=self._we)
