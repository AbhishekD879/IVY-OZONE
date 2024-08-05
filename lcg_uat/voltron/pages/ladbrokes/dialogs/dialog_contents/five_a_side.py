from voltron.pages.shared.dialogs.dialog_base import Dialog
from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.utils.waiters import wait_for_result


class FiveASide(Dialog):
    _stay = 'xpath=.//button[@data-crlat="button.Stay"]'
    _leave = 'xpath=.//button[@data-crlat="button.Leave"]'
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
    def leave(self):
        return ButtonBase(selector=self._leave, context=self._we)

    @property
    def stay(self):
        return ButtonBase(selector=self._stay, context=self._we)

    @property
    def ok_thanks_btn(self):
        wait_for_result(
            lambda: self._find_elements_by_selector(selector=self._ok_thanks_btn, context=self._we) is not None,
            expected_result=True)
        return ButtonBase(selector=self._ok_thanks_btn, context=self._we)
