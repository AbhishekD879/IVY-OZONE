import tests
from datetime import datetime, timedelta
from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.primitives.inputs import InputBase


class HistoryTableItems(ComponentBase):
    _payment_type = 'xpath=.//*[contains(@class,"payment-type")]/strong'
    _name = 'xpath=.//*[contains(@class,"payment-type")]/span'
    _amount = 'xpath=.//*[contains(@class,"right-align")]/span[@class]'
    _transaction_type = 'xpath=.//*[contains(@class,"right-align")]/span/following-sibling::span'
    _collapse_body = 'xpath=.//*[@class="collapsible-body"]'

    @property
    def payment_type(self):
        return self._find_element_by_selector(selector=self._payment_type)

    @property
    def name(self):
        return self._find_element_by_selector(selector=self._name)

    @property
    def amount(self):
        return self._find_element_by_selector(selector=self._amount)

    @property
    def transaction_type(self):
        return self._find_element_by_selector(selector=self._transaction_type)

    @property
    def collapse_body(self):
        return self._find_element_by_selector(selector=self._collapse_body)


class HistoryTable(ComponentBase):
    _item = 'xpath=.//li'
    _list_item_type = HistoryTableItems


class InfoToolTip(ComponentBase):
    _info_text = 'xpath=.//p'
    _info_ok = 'xpath=.//button'

    @property
    def deposit_text(self):
        return self._find_element_by_selector(selector=self._info_text)

    @property
    def info_ok_button(self):
        return self._find_element_by_selector(selector=self._info_ok)


class NetDeposit(ComponentBase):
    _deposit_text = 'xpath=.//*[@class="text-bold"]'
    _deposit_tool_tip = 'xpath=.//*[@id="net-deposit-tooltip"]'

    @property
    def deposit_text(self):
        return self._find_element_by_selector(selector=self._deposit_text)

    @property
    def deposit_tool_tip(self):
        return self._find_element_by_selector(selector=self._deposit_tool_tip)


class HistoryDate(ComponentBase):
    _from_date = 'xpath=.//div[contains(@class,"date-picker")]//*[@id="fdate"]'
    _to_date = 'xpath=.//div[contains(@class,"date-picker")]//*[@id="tdate"]'

    @property
    def from_date_drop_down(self):
        return InputBase(selector=self._from_date, context=self._we)

    @property
    def from_date(self):
        return self.from_date_drop_down.value

    @from_date.setter
    def from_date(self, value):
        if tests.settings.brand == 'bma' and tests.settings.backend_env == 'prod':
            strf_time = "%m/%d/%Y"
        else:
            strf_time = "%d/%m/%Y"
        added_value = datetime.now() + timedelta(days=value)
        updated_value = added_value.strftime(strf_time)
        self.from_date_drop_down.value = updated_value

    @property
    def to_date_drop_down(self):
        return InputBase(selector=self._to_date, context=self._we)

    @property
    def to_date(self):
        return self.to_date_drop_down.value

    @to_date.setter
    def to_date(self, value):
        if tests.settings.brand == 'bma' and tests.settings.backend_env == 'prod':
            strf_time = "%m/%d/%Y"
        else:
            strf_time = "%d/%m/%Y"
        added_value = datetime.now() + timedelta(days=value)
        updated_value = added_value.strftime(strf_time)
        self.to_date_drop_down.value = updated_value


class AllPaymentHistory(ComponentBase):
    _payment_option = 'xpath=.//*[@id="paymentOption"]'
    _other_options = 'xpath=.//option'

    @property
    def payment_option(self):
        return self._find_element_by_selector(selector=self._payment_option)

    @property
    def payment_option_list(self):
        options = self._find_elements_by_selector(selector=self._other_options)
        return [option.text for option in options]

    def click_option(self, value=None):
        options = self._find_elements_by_selector(selector=self._other_options)
        if value:
            for option in options:
                if option.text == value:
                    option.click()
                    break


class PaymentHistory(ComponentBase):
    _transaction_options = 'xpath=.//*[contains(@class,"transaction-type-tab")]'
    _all_payment_history = 'xpath=.//*[@id="txnSearchForm"]'
    _all_payment_history_type = AllPaymentHistory
    _history_date = 'xpath=.//*[@id="all-payment-history"]//div/following-sibling::div'
    _history_date_type = HistoryDate
    _go_button = 'xpath=.//*[@class="btn active-btn"]'
    _net_deposit = 'xpath=.//*[@class="net-deposits"]'
    _net_deposit_type = NetDeposit
    _info_tool_tip = 'xpath=.//*[@class="qtip-content"]'
    _info_tool_tip_type = InfoToolTip
    _history_table = 'xpath=.//*[contains(@class,"history-table")]'
    _history_table_type = HistoryTable

    @property
    def transaction_options(self):
        return self._find_elements_by_selector(selector=self._transaction_options)

    def click_transaction_option(self, value):
        options = self.transaction_options
        for option in options:
            if option.text == value:
                option.click()
                break

    @property
    def net_deposit(self):
        return self._net_deposit_type(selector=self._net_deposit)

    @property
    def all_payment_history(self):
        return self._all_payment_history_type(selector=self._all_payment_history)

    @property
    def history_date(self):
        return self._history_date_type(selector=self._history_date)

    @property
    def go_button(self):
        return self._find_element_by_selector(selector=self._go_button)

    @property
    def deposit_info(self):
        return self._info_tool_tip_type(selector=self._info_tool_tip)

    @property
    def history_table(self):
        return self._history_table_type(selector=self._history_table)
