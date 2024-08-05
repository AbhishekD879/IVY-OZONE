from collections import OrderedDict

from selenium.common.exceptions import UnexpectedTagNameException

import tests
from voltron.pages.shared.contents.base_contents.common_base_components.tab_content import TabContent
from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.date_picker import DatePicker
from voltron.pages.shared.components.primitives.amount_field import AmountField
from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.pages.shared.components.primitives.text_labels import TextBase
from voltron.pages.shared.contents.base_contents.common_base_components.tabs_menu import TabsMenu
from voltron.pages.shared.contents.my_bets.bet_history.bet_history import BetHistory
from selenium.webdriver.support.select import Select


class TransactionDateFilters(ComponentBase, Select):
    def __init__(self, *args, **kwargs):
        ComponentBase.__init__(self, *args, **kwargs)
        try:
            Select.__init__(self, webelement=self._we)
        except UnexpectedTagNameException:
            pass


class TransactionData(ComponentBase):
    _date = 'xpath=.//*[@data-crlat="transaction.date"]'
    _date_type = TextBase
    _payment_account = 'xpath=.//*[@data-crlat="transaction.account"]'
    _fade_out_overlay = True

    @property
    def date(self):
        return self._date_type(selector=self._date, context=self._we)

    @property
    def payment_account(self):
        return self._get_webelement_text(selector=self._payment_account)


class TransactionAmount(TextBase):

    @property
    def value(self):
        return AmountField(selector=self._value, context=self._we)


class TransactionHistoryItem(ComponentBase):
    _payment_image = 'xpath=.//*[@data-crlat="img.payment"]'
    _transaction_data = 'xpath=.//*[@data-crlat="transaction.data"]'
    _transaction_data_type = TransactionData
    _amount = 'xpath=.//*[@data-crlat="amount"]'
    _amount_type = TransactionAmount
    _cancel_button = 'xpath=.//*[@data-crlat="cancel"]'

    @property
    def name(self):
        return self.transaction_data.date.value + ' ' + self.amount.value.value

    @property
    def transaction_data(self):
        return self._transaction_data_type(selector=self._transaction_data, context=self._we)

    @property
    def payment_image(self):
        return ComponentBase(selector=self._payment_image, timeout=1)

    @property
    def amount(self):
        # so amount label is amount.label, value is amount.value.value, currency is amount.value.currency
        return self._amount_type(selector=self._amount, context=self._we)

    @property
    def cancel_button(self):
        return ButtonBase(selector=self._cancel_button, timeout=1)


class SummarySectionTextBase(TextBase):

    @property
    def name(self):
        return self.label


class SummarySection(ComponentBase):
    _item = 'xpath=.//*[@data-crlat="summary.item"]'
    _list_item_type = SummarySectionTextBase
    _question_image = 'xpath=.//*[@data-crlat="img.question"]'
    _verify_spinner = True

    @property
    def question_image(self):
        return ButtonBase(selector=self._question_image, context=self._we, timeout=1)


class Transactions(ComponentBase):
    _item = 'xpath=.//*[@data-crlat="transactions.item"]'
    _list_item_type = TransactionHistoryItem


class TransactionHistoryTabContent(TabContent):
    _tabs_menu = 'xpath=.//*[@data-crlat="panel.tabs"]'
    _tabs_menu_type = TabsMenu
    _accordions_list = 'xpath=.//*[@data-crlat="accordionsList" and not(featured-quick-links)]'
    _accordions_list_type = Transactions
    _date_picker = 'xpath=.//*[@class="datepickers-section"]'
    _date_picker_type = DatePicker
    _no_history_message = 'xpath=.//*[@data-crlat="textMsg"]'
    _summary_section = 'xpath=.//*[@data-crlat="summarySection"]'
    _contact_info = 'xpath=.//*[@data-crlat="contactInfo"]'
    _contact_info_type = ComponentBase
    _verify_spinner = True

    @property
    def tabs_menu(self):
        return self._tabs_menu_type(selector=self._tabs_menu, context=self._we)

    @property
    def date_picker(self):
        return DatePicker(selector=self._date_picker, context=self._we)

    @property
    def contact_information(self):
        return self._contact_info_type(selector=self._contact_info, context=self._we)

    @property
    def no_transaction_history_message(self):
        return self._get_webelement_text(selector=self._no_history_message)

    @property
    def summary_section(self):
        return SummarySection(selector=self._summary_section, context=self._we, timeout=3)


class TransactionHistory(BetHistory):
    # _url_pattern = r'^http[s]?:\/\/.+\/transaction-history'
    _url_pattern = r'^http[s]?:\/\/.+\/'
    _transaction_history = 'xpath=.//*[@id="monthly-content"]'
    _back_button = 'xpath=.//*[contains(@class, "ui-back")]'
    _transaction_message = 'xpath=.//*[@class="message-panel"]//*[@class="cms-container"]'
    _tab_content_type = TransactionHistoryTabContent
    _stake_returns = 'xpath=.//*[@id="stakes-returns"]'
    _transaction_entries = 'xpath=.//*[contains(@class, "transaction")]'
    _date_filter = 'xpath=.//*[contains(@class, "form-base")]//select'


    @property
    def transaction_date_filter(self):
        return TransactionDateFilters(selector=self._date_filter, timeout=2)

    @property
    def transaction_data(self):
        return self._find_element_by_selector(selector=self._transaction_history, timeout=1) is not None

    @property
    def back_button(self):
        return ButtonBase(selector=self._back_button, context=self._we, timeout=1)

    @property
    def transaction_message(self):
        return self._get_webelement_text(selector=self._transaction_message, timeout=1) is not None

    @property
    def stake_returns(self):
        return StakeInfo(selector=self._stake_returns, context=self._we, timeout=1)

    @property
    def transaction_entries(self):
        return self._find_elements_by_selector(selector=self._transaction_entries, timeout=3)

    @property
    def transaction_history_items(self):
        _history_item = 'xpath=.//lh-navigation-layout-top-menu-v2//*[contains(@class,"nav-item")]' \
            if tests.settings.device_type != 'mobile' else \
            'xpath=.//vn-am-menu-item/vn-menu-item/a[contains(@class,"menu-item-link")]'
        items_we = self._find_elements_by_selector(selector=_history_item, context=self._we, timeout=self._timeout)
        items_ordered_dict = OrderedDict()
        for item_we in items_we:
            list_item = ButtonBase(web_element=item_we)
            list_item.scroll_to()
            items_ordered_dict.update({list_item.name: list_item})
        return items_ordered_dict


class StakeInfo(ComponentBase):
    _stake_lables = 'xpath=.//*[@class="trn-head txt-xs"]'
    _stake_values = 'xpath=.//*[@class="trn-bold"]/td'

    @property
    def stake_lables(self):
        return self._find_elements_by_selector(selector=self._stake_lables, timeout=3)

    @property
    def stake_values(self):
        return self._find_elements_by_selector(selector=self._stake_values, timeout=3)
