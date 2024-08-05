from voltron.pages.shared.components.header_desktop import DesktopHeader


class GlobalHeaderDesktopLadbrokes(DesktopHeader):
    _sign_in = 'xpath=.//vn-h-button//*[contains(@class, "btn-secondary")]'
    _join_us = 'xpath=.//vn-h-button//*[contains(@class, "btn-primary")]'
    _brand_logo = 'xpath=.//vn-h-logo//a'

    @property
    def brand_logo(self):
        return self._brand_logo_type(selector=self._brand_logo, context=self._we, timeout=2)
