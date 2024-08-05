from voltron.pages.shared.components.primitives.buttons import SpinnerButtonBase
from voltron.pages.shared.dialogs.dialog_base import Dialog


class VerifyYourAccount(Dialog):
    _verify_me_button = 'xpath=.//*[@data-crlat="verifyMeButton"]'

    @property
    def verify_me_now_button(self):
        return SpinnerButtonBase(selector=self._verify_me_button, context=self._we)
