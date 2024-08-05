from voltron.pages.coral.components.header import CoralMobileHeader
from voltron.pages.shared.components.primitives.buttons import ButtonBase


class GlobalHeaderLadbrokes(CoralMobileHeader):
    _button_count = 'xpath=.//vn-h-button'
    _join_us = 'xpath=.//vn-h-button//*[contains(@class, "btn-primary")]'
    _sign_in = 'xpath=.//vn-h-button//*[contains(@class, "btn-secondary")]'
    _back_button = 'xpath=.//*[@data-crlat="btnBack"]'
    _gambling = 'xpath=.//vn-h-button//*[contains(@class, "theme-safer-gambling")]'

    @property
    def sign_in_join_button(self):
        context = ButtonBase(selector=self._join_us, context=self._we, timeout=2)
        context.is_displayed()
        return context

    @property
    def sign_in(self):
        buttons_count = list(self._find_elements_by_selector(selector=self._button_count, timeout=4))
        section = self._find_element_by_selector(selector=self._gambling, context=self._we)
        if section:
            return self.sign_in_join_button if len(buttons_count) == 2 else self.sign_in_button
        else:
            return self.sign_in_join_button if len(buttons_count) == 1 else self.sign_in_button

    @property
    def join_us(self):
        buttons_count = list(self._find_elements_by_selector(selector=self._button_count, timeout=4))
        if len(buttons_count) == 1:
            return self.sign_in_join_button
        else:
            return self.join_us_button

    @property
    def sign_in_button(self):
        context = ButtonBase(selector=self._sign_in, context=self._we, timeout=3)
        context.is_displayed()
        return context

    @property
    def join_us_button(self):
        context = ButtonBase(selector=self._join_us, context=self._we, timeout=3)
        context.is_displayed()
        return context

    @property
    def back_button(self):
        return ButtonBase(selector=self._back_button, context=self._we, timeout=3)

    @property
    def has_back_button(self):
        return self._find_element_by_selector(selector=self._back_button, timeout=4) is not None
