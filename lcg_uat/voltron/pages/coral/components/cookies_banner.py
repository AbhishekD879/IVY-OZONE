from voltron.pages.shared.components.cookie_banner import CookieBanner
from voltron.pages.shared.components.primitives.buttons import ButtonBase


class BMACookieBanner(CookieBanner):
    _description = 'xpath=.//*[@data-crlat="cookieDescription"] | .//*[@id="onetrust-group-container"]'
    _ok_button = 'xpath=.//*[contains(text(), "OK")] | .//*[@id="onetrust-accept-btn-handler"]'
    _cookies_setting_link = 'xpath=.//*[contains(@class, "pc-txt")] | .//*[@id="onetrust-pc-btn-handler"]'

    @property
    def ok_button(self):
        return ButtonBase(selector=self._ok_button, context=self._we)

    @property
    def description(self):
        return self._description_type(selector=self._description)

    @property
    def cookies_setting_link(self):
        return ButtonBase(selector=self._cookies_setting_link, context=self._we)
