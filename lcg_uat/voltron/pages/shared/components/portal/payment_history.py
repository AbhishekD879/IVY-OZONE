from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.pages.shared.components.primitives.text_labels import TextBase


class PaymentHistory(ComponentBase):
    _url_pattern = r'^http[s]?:\/\/.+\/en/cashier/transaction-history'
    _url_matcher_timeout = 20
    _header = 'xpath=.//*[@id="cashierHeader"]'
    _content = 'xpath=.//app-transaction-history'

    @property
    def header(self):
        return PaymentHistoryHeader(selector=self._header, timeout=2, context=self._we)

    @property
    def content(self):
        return PaymentHistoryContent(selector=self._content, timeout=2, context=self._we)


class PaymentHistoryHeader(ComponentBase):
    _brand_logo = 'xpath=.//button[contains(@class, "Brand")]'
    _header_title = 'xpath=.//*[contains(@class, "cashier-page-heading")]'
    _balance = 'xpath=.//*[contains(@class, "total-balance")]'
    _close_button = 'xpath=.//*[contains(@class, "ui-close")]'

    @property
    def brand_logo(self):
        return ButtonBase(selector=self._brand_logo, timeout=2, context=self._we)

    @property
    def header_title(self):
        return TextBase(selector=self._header_title, timeout=2, context=self._we)

    @property
    def balance(self):
        return TextBase(selector=self._balance, timeout=2, context=self._we).text.upper().replace("GBP", "")

    @property
    def close_button(self):
        return ButtonBase(selector=self._close_button, timeout=2, context=self._we)


class PaymentHistoryContent(ComponentBase):
    _transaction_filters = 'xpath=.//transaction-history-filter-tabs'
    _account_info = 'xpath=.//*[@class="account-info"]'

    @property
    def transaction_filters(self):
        return PaymentHistoryTransactionFilter(selector=self._transaction_filters, context=self._we, timeout=2)

    @property
    def account_info(self):
        return PaymentHistoryAccountInfo(selector=self._account_info, context=self._we, timeout=2)


class PaymentHistoryAccountInfoItem(ComponentBase):
    _icon = 'xpath=.//*[contains(@class,"icon")]'
    _text = 'xpath=.//*[contains(@class,"account-info-text")]'
    _amount_value = 'xpath=.//*[contains(@class,"float-left")]/following-sibling::div[contains(@class,"amount")]'

    @property
    def name(self):
        return self.text.text

    @property
    def icon(self):
        return self._find_elements_by_selector(selector=self._icon, context=self._we)

    @property
    def amount(self):
        return TextBase(selector=self._amount_value, context=self._we, timeout=2)

    @property
    def text(self):
        return TextBase(selector=self._text, timeout=2, context=self._we)


class PaymentHistoryAccountInfo(ComponentBase):
    _last_days = 'xpath=.//*[contains(@class,"account-date-info")]//p[contains(@class,"date-info-text")]'
    _edit_date = 'xpath=.//*[contains(@class,"edit-date")]'
    _item = 'xpath=.//*[contains(@class,"account-info-inner")]/div[contains(@class,"account-info")]'
    _list_item_type = PaymentHistoryAccountInfoItem

    @property
    def last_days(self):
        return TextBase(selector=self._last_days, timeout=2, context=self._we)

    @property
    def edit_date(self):
        return ButtonBase(selector=self._edit_date, timeout=2, context=self._we)


class FilterPill(ButtonBase):
    _filter_icon = 'xpath=.//*[contains(@class,"pill-image")]'
    _filter_text = 'xpath=.//*[contains(@class,"badge-text")]'

    @property
    def filter_icon(self):
        return self._find_elements_by_selector(selector=self._filter_icon, context=self._we, timeout=2)

    @property
    def filter_name(self):
        return TextBase(selector=self._filter_text, context=self._we, timeout=2)

    @property
    def name(self):
        return self.filter_name.text


class PaymentHistoryTransactionFilter(ComponentBase):
    _item = 'xpath=.//*[contains(@class,"pill-with-badge-v2")]'
    _list_item_type = FilterPill
