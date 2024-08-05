from collections import OrderedDict

from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.bet_receipt_info import BetReceiptInfo
from voltron.pages.shared.components.primitives.amount_field import AmountField
from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.pages.shared.contents.base_contents.common_base_components.event_group import EventGroup
from voltron.pages.shared.contents.my_bets.cashout import Bet, BetDetails
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.waiters import wait_for_result


class EditAccaHistory(Bet, EventGroup):
    # _bet_receipt_info = 'xpath=.//*[@data-crlat="betReceiptInfo"]'
    _bet_receipt_info = 'xpath=.//*[contains(@class,"betDetailsAccordion-lads")] | .//*[contains(@class,"betDetailsAccordion-coral")]/*[@data-crlat="accordion"]'
    _cash_out_history = 'xpath=.//*[@data-crlat="cashOutHistory"]'

    def _wait_active(self, timeout=0):
        """
        Waits for component's content to be loaded.
        """
        self._we = self._find_myself()
        wait_for_result(lambda: self._find_element_by_selector(self._bet_receipt_info, context=self._we) is not None,
                        name='Waiting for receipt info to be present',
                        timeout=5)

    @property
    def items_as_ordered_dict(self) -> OrderedDict:
        items_we = self._wait_all_items()
        self._logger.debug(
            f'*** Found {len(items_we)} {self.__class__.__name__} - {self._list_item_type.__name__} items')
        items_ordered_dict = OrderedDict()
        for item_we in items_we:
            list_item = self._list_item_type(web_element=item_we)
            items_ordered_dict.update({list_item.name: list_item})
        return items_ordered_dict

    @property
    def bet_receipt_info(self):
        if not self.bet_details.is_expanded():
            self.bet_details.chevron_arrow.click()
            wait_for_result(lambda: self.bet_details.is_expanded is True,
                            name='Bet Details Expanded',
                            expected_result=True,
                            timeout=10)
        return BetDetails(selector=self._bet_receipt_info, context=self._we)
        # return BetReceiptInfo(selector=self._bet_receipt_info, context=self._we)

    @property
    def cash_out_history(self):
        return CashOutHistory(selector=self._cash_out_history, context=self._we)

    @property
    def name(self):
        return self._get_webelement_text(we=self._we).replace('\n', ' ')


class HistoryBets(ComponentBase):
    _edit_acca_history_holder = 'xpath=.//ancestor::*[@data-crlat="betContainer"]'
    _name = 'xpath=.//*[@data-crlat="betType"]'
    _date = 'xpath=.//*[@data-crlat="time"]'
    _type = 'xpath=.//*[@data-crlat="histLbl"]'

    @property
    def content(self):
        return EditAccaHistory(selector=self._edit_acca_history_holder, context=self._we)

    @property
    def name(self):
        return self._get_webelement_text(self._name, context=self._we)

    @property
    def date(self):
        return self._get_webelement_text(self._date, context=self._we)

    @property
    def type(self):
        return self._get_webelement_text(self._type, context=self._we)


class EditAccaHistoryHolder(ComponentBase):
    _acca_history_body = 'xpath=.//*[@data-crlat="drawer.body"]'
    _close_button = 'xpath=.//*[@data-crlat="drawer.closeButton"]'
    _header = 'xpath=.//*[@data-crlat="drawer.header"]'

    def _wait_active(self, timeout=0):
        """
        Waits for component's content to be loaded.
        """
        self._we = self._find_myself()
        # For some reason, element already present in the DOM, but it's text is '' for some short period of the time
        wait_for_result(lambda: self.header_text != '',
                        name='Waiting for header to be present',
                        timeout=5)

    @property
    def content(self):
        return EditAccaHistoryBody(selector=self._acca_history_body, context=self._we, timeout=3)

    @property
    def header_text(self):
        return self._get_webelement_text(self._header, context=self._we)

    @property
    def close_button(self):
        return ButtonBase(selector=self._close_button, context=self._we)


class EditAccaHistoryBody(ComponentBase):
    _item = 'xpath=.//*[@data-crlat="cashout.item.header"]'
    _list_item_type = HistoryBets

    def _wait_active(self, timeout=0):
        """
        Waits for component's content to be loaded.
        """
        self._we = self._find_myself()
        wait_for_result(lambda: self._find_element_by_selector(self._item, context=self._we) is not None,
                        name='Waiting for headers to be present',
                        timeout=5)

    @property
    def headers(self):
        items_we = self._find_elements_by_selector(selector=self._item, context=self._we)
        self._logger.debug(
            f'*** Found {len(items_we)} {self.__class__.__name__} - {self._list_item_type.__name__} items')
        items_ordered_dict = OrderedDict()
        for item_we in items_we:
            list_item = self._list_item_type(web_element=item_we)
            items_ordered_dict.update({list_item.name: list_item})
        return items_ordered_dict


class AccaHistoryAmountField(AmountField):

    def __get_full_text(self):
        text = self._get_webelement_text(we=self._we, timeout=1)
        if not text:
            raise VoltronException('Cannot get text for %s' % self.__class__.__name__)
        return text.split('\n')

    @property
    def _text(self):
        return self.__get_full_text()[-1]

    @property
    def message(self):
        return self.__get_full_text()[0]


class CashOutHistory(ComponentBase):
    _stake_used = 'xpath=.//*[@data-crlat="stakeUsed"]'
    _cash_out_amount = 'xpath=.//*[@data-crlat="cashoutValue"]'
    _cash_out_used_msg = 'xpath=.//*[@data-crlat="cashOutUsedMsg"]'

    @property
    def stake_used(self):
        return AccaHistoryAmountField(selector=self._stake_used, context=self._we)

    @property
    def cash_out(self):
        return AccaHistoryAmountField(selector=self._cash_out_amount, context=self._we)

    @property
    def cash_out_used_message(self):
        return self._get_webelement_text(selector=self._cash_out_used_msg, context=self._we)
