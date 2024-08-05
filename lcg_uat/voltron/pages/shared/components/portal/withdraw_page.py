from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.pages.shared.components.primitives.text_labels import TextBase


class CashierWithdraw(ComponentBase):
    _url_pattern = r'^http[s]?:\/\/.+\/en/cashier/withdrawal'
    _url_matcher_timeout = 20
    _header = 'xpath=.//*[@id="cashierHeader"]'
    _content = 'xpath=.//*[@id="WithdrawlPageWrapper"]'

    @property
    def header(self):
        return CashierHeader(selector=self._header, timeout=2)

    def content(self):
        return WithdrawContent(selector=self._content, timeout=2)


class CashierHeader(ComponentBase):
    _brand_logo = 'xpath=.//button[contains(@class, "Brand")]'
    _header_title = 'xpath=.//*[contains(@class, "cashier-page-heading")]'
    _balance = 'xpath=.//*[contains(@class, "total-balance")]'
    _close_button = 'xpath=.//*[contains(@class, "ui-close")]'

    @property
    def brand_logo(self):
        return ButtonBase(selector=self._brand_logo, timeout=2)

    @property
    def header_title(self):
        return TextBase(selector=self._header_title, timeout=2)

    @property
    def balance(self):
        return TextBase(selector=self._balance, timeout=2).text.upper().replace("GBP", "")

    @property
    def close_button(self):
        return ButtonBase(selector=self._close_button, timeout=10)


class WithdrawContent(ComponentBase):
    pass
