from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.pages.shared.dialogs.dialog_base import Dialog


class YouAreBetting(Dialog):
    _online_button = 'xpath=.//*[@data-crlat="onlineBtn"]'
    _bet_here = 'xpath=.//*[@data-crlat="onlineLabel"]'
    _inshop_button = 'xpath=.//*[@data-crlat="inshopBtn"]'
    _save_for_later = 'xpath=.//*[@data-crlat="inshopLbl"]'
    _default_action = 'close_dialog'

    def scroll_to_we(self, web_element=None):
        """
        Bypassing scroll to dialog as it's on view
        """
        pass

    @property
    def online_button(self):
        return ButtonBase(selector=self._online_button, context=self._we)

    @property
    def bet_here(self):
        return self._get_webelement_text(selector=self._bet_here, timeout=1).strip()

    @property
    def inshop_button(self):
        return ButtonBase(selector=self._inshop_button, context=self._we)

    @property
    def save_for_later(self):
        return self._get_webelement_text(selector=self._save_for_later, timeout=1).strip()
