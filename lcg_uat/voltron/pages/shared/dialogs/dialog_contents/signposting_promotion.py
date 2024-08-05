from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.pages.shared.dialogs.dialog_base import Dialog


class SignPostingPromotion(Dialog):
    _ok_button = 'xpath=.//*[@data-crlat="okButton"]'
    _more_button = 'xpath=.//*[@data-crlat="moreButton"]'
    _default_action = 'click_ok'
    _text = 'xpath=.//*[@data-crlat="promoText"]'

    @property
    def has_ok_button(self):
        return self._get_webelement_text(selector=self._ok_button, timeout=.5)

    @property
    def has_more_button(self):
        return self._get_webelement_text(selector=self._more_button, timeout=.5)

    @property
    def more_button(self):
        return ButtonBase(selector=self._more_button, context=self._we)

    @property
    def ok_button(self):
        return ButtonBase(selector=self._ok_button, context=self._we)

    def click_ok(self):
        self.ok_button.click()

    def default_action(self):
        self.click_ok()

    @property
    def text(self):
        return self._get_webelement_text(selector=self._text, timeout=1)
