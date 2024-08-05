from voltron.pages.ladbrokes.components.header_desktop import GlobalHeaderDesktopLadbrokes
from voltron.pages.shared.components.primitives.buttons import ButtonBase


class GlobalHeaderTabletLadbrokes(GlobalHeaderDesktopLadbrokes):
    _sign_in_join_button = 'xpath=.//vn-h-button//*[contains(@class, "btn-primary")]'
    _back_button = 'xpath=.//*[@data-crlat="btnBack"]'

    @property
    def sign_in_join_button(self):
        context = ButtonBase(selector=self._sign_in_join_button, context=self._we, timeout=2)
        context.is_displayed()
        return context

    @property
    def sign_in(self):
        return self.sign_in_join_button

    @property
    def join_us(self):
        return self.sign_in_join_button

    @property
    def back_button(self):
        return ButtonBase(selector=self._back_button, context=self._we, timeout=3)

    @property
    def has_back_button(self):
        return self._find_element_by_selector(selector=self._back_button, timeout=4) is not None
