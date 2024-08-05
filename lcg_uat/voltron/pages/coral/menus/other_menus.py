from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.content_header import HeaderLine, PageTitle
from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.pages.shared.components.primitives.text_labels import TextBase
from voltron.pages.shared.menus.right_menu import RightMenuItemLink
# todo:     VOL-5541  CoralMenus / other_menus.py should be moved to shared and renamed


class PaymentHistoryHeader(ComponentBase):
    _close_button = 'xpath=.//*[contains(@class, "close-button")]'

    @property
    def close_button(self):
        return ButtonBase(selector=self._close_button, context=self._we)


class SpecificHeader(ComponentBase):
    _back_button = 'xpath=.//span[contains(@class, "ui-back")]'
    _close_button = 'xpath=.//span[contains(@class, "ui-close")]'
    _page_title = 'xpath=.//div[contains(@class, "header-ctrl-txt")]'
    _page_title_type = PageTitle

    @property
    def back_button(self):
        return ButtonBase(selector=self._back_button, context=self._we)

    @property
    def close_button(self):
        return ButtonBase(selector=self._close_button, context=self._we)

    @property
    def page_title(self):
        return self._page_title_type(selector=self._page_title)


class InboxHeader(ComponentBase):
    _back_button = 'xpath=.//span[contains(@class, "ui-back")]'
    _close_button = 'xpath=.//span[contains(@class, "ui-close")]'

    @property
    def back_button(self):
        return ButtonBase(selector=self._back_button, context=self._we)

    @property
    def close_button(self):
        return ButtonBase(selector=self._close_button, context=self._we)


class HelpContactHeader(ComponentBase):
    _icon = 'xpath=.//div[contains(@class, "helpcontact-mainheader")]'

    @property
    def icon(self):
        return TextBase(selector=self._icon, context=self._we)


class ExternalPageComponentWrapper:
    _payment_history_header = 'xpath=.//*[contains(@class, "main-header")]'
    _payment_history_header_type = PaymentHistoryHeader
    _specific_header = 'xpath=.//lh-header-bar'
    _specific_header_type = SpecificHeader
    _inbox_header = 'xpath=.//lh-header-bar'
    _inbox_header_type = InboxHeader
    _help_contact_header = 'xpath=.//div[contains(@class, "main-heading")]'
    _help_contact_type = HelpContactHeader
    _header_line = 'xpath=.//*[@data-crlat="topBar"] | .//*[@data-crlat="topBarBetslipOpenBets"]'
    _header_line_type = HeaderLine

    @property
    def payment_history_header(self):
        return self._payment_history_header_type(selector=self._payment_history_header)

    @property
    def specific_header(self):
        return self._specific_header_type(selector=self._specific_header)

    @property
    def header(self):
        header_line = self._header_line_type(selector=self._header_line)
        header_line.is_displayed(timeout=3)
        return header_line

    @property
    def inbox_header(self):
        return self._inbox_header_type(selector=self._inbox_header)

    @property
    def help_contact_header(self):
        return TextBase(selector=self._help_contact_header)


class CoralMenuItem(ComponentBase):
    _name = 'xpath=.//*[contains(@class, "list-nav-txt")]'
    _link = 'xpath=.//a[contains(@class, "menu-item-link")] | .//a[contains(@class, "menu-item-link list-nav-link")]'
    _link_type = RightMenuItemLink
    _header_type = ExternalPageComponentWrapper

    @property
    def link(self):
        return self._link_type(selector=self._link, context=self._we, timeout=3)

    def click(self):
        self.link.click()

    @property
    def get_header(self):
        # Return header of the outer page
        return self._header_type()

    @property
    def name(self):
        return self._get_webelement_text(selector=self._name)


class CoralMenus(ComponentBase):
    _item = 'xpath=.//vn-am-icon-menu | .//vn-am-menu-item'
    _list_item_type = CoralMenuItem
    _withdrawal = 'xpath=.//div[contains(@class, "v6-theme")]'

    @property
    def withdrawal(self):
        return CoralWithdrawal(selector=self._withdrawal, context=self._we)


class CoralWithdrawal(ComponentBase):
    _url_pattern = '^http[s]?:\/\/.+\/cashout'
    _header = 'xpath=.//header[@class = "main-header"]'

    @property
    def header(self):
        return CoralWithdrawalHeader(selector=self._header, context=self._we)


class CoralWithdrawalHeader(ComponentBase):
    _close_button = 'xpath=.//*[contains(@class, "close-button")]'

    @property
    def close_button(self):
        return ButtonBase(selector=self._close_button, context=self._we)
