from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.pages.shared.components.primitives.text_labels import LinkBase
from voltron.pages.shared.dialogs.dialog_base import Dialog


class GoodNews(Dialog):
    _text = 'xpath=.//*[@data-crlat="text"]'
    _link = 'xpath=.//a'  # data-crlat can't be added
    _accept_button = 'xpath=.//*[@data-crlat="dialog.accept" or @data-uat="popUpButton"]'
    _default_action = 'click_accept'

    @property
    def link(self):
        return LinkBase(selector=self._link, context=self._we)

    @property
    def text(self):
        return self._get_webelement_text(selector=self._text, timeout=1).strip()

    @property
    def accept_button(self):
        return ButtonBase(selector=self._accept_button, context=self._we)

    def click_accept(self):
        self.accept_button.click()
