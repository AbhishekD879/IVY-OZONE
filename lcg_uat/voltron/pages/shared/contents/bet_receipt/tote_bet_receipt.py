from collections import OrderedDict

from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.pages.shared.components.primitives.stake import Stake
from voltron.pages.shared.contents.edp.racing_edp_market_section import Outcome
from voltron.pages.shared.contents.edp.racing_event_details import EventMarketsList
from voltron.utils.waiters import wait_for_result


class ToteReceiptStake(Stake):
    _value = 'xpath=.//*[@data-crlat="betReceipt.stakeAmount"]'


class BetReceiptOutcomePart(ComponentBase):
    @property
    def name(self):
        return self._get_webelement_text(we=self._we)


class BetReceiptOutcome(Outcome):
    _expanded_summary = 'xpath=.//*[@data-crlat="betReceipt.expandedSummary"]'
    _bet_name = 'xpath=.//*[@data-crlat="betReceipt.betPoolTitle"]'
    _expand_plus_icon = 'xpath=.//*[@data-crlat="toggleIcon"]'

    _outcome_name = 'xpath=.//*[@data-crlat="betReceipt.outcomeName"]'
    _item = _outcome_name
    _list_item_type = BetReceiptOutcomePart
    _bet_leg = 'xpath=.//*[@data-crlat="betReceipt.betLeg"]'
    _bet_id = 'xpath=.//*[@data-crlat="betReceipt.betID"]'
    _stake = 'xpath=.//*[@data-crlat="betReceipt.Stake"]'

    @property
    def bet_receipt_title(self):
        return self._get_webelement_text(selector=self._bet_name)

    @property
    def expand_plus_icon(self):
        return self._find_element_by_selector(selector=self._expand_plus_icon, context=self._we)

    def expand(self):
        self.scroll_to_we()
        if self.is_expanded():
            self._logger.debug(f'*** Bypassing accordion expand, since "{self.bet_receipt_title}" already expanded')
        else:
            self._logger.debug(f'*** Expanding "{self.bet_receipt_title}"')
            self.expand_plus_icon.click()
            wait_for_result(lambda: self.is_expanded(), name=f'{self.__class__.__name__} Expanded status', timeout=5)

    def is_expanded(self):
        web_element = self._find_element_by_selector(selector=self._expanded_summary, context=self._we, timeout=0.3)
        return web_element is not None

    @property
    def stake(self):
        return ToteReceiptStake(selector=self._stake, context=self._we)

    @property
    def outcome_name(self):
        return self._get_webelement_text(selector=self._outcome_name, context=self._we)

    @property
    def bet_leg(self):
        return self._get_webelement_text(selector=self._bet_leg, context=self._we)

    @property
    def bet_id(self):
        return self._get_webelement_text(selector=self._bet_id, context=self._we)

    @property
    def items_as_ordered_dict(self) -> OrderedDict:
        items_we = self._find_elements_by_selector(selector=self._item, context=self._we)
        self._logger.debug(f'*** Found {len(items_we)} {self.__class__.__name__} - {self._list_item_type.__name__} items')
        items_ordered_dict = OrderedDict()
        for item_we in items_we:
            list_item = self._list_item_type(web_element=item_we)
            items_ordered_dict.update({list_item.name: list_item})
        return items_ordered_dict


class ToteBetReceiptSection(EventMarketsList):
    _item = 'xpath=.//*[@data-crlat="betReceipt.betItem"]'
    _list_item_type = BetReceiptOutcome

    @property
    def name(self):
        return self._get_webelement_text(we=self._we)


class ToteBetReceiptSectionsList(EventMarketsList):
    _item = 'xpath=.//*[@data-crlat="betReceiptContent"]'
    _list_item_type = ToteBetReceiptSection
    _success_bet_message = 'xpath=.//*[@data-crlat="betReceipt.successMsg"]'
    _failed_bet_receipt_data = 'xpath=.//*[@data-crlat="betReceipt.failedMsgData"]'
    _failed_message = 'xpath=.//*[@data-crlat="betReceipt.failedMsg"]'
    _bet_rules = 'xpath=.//*[@data-crlat="betReceipt.bettingRules"]'
    _continue_btn = 'xpath=.//*[@data-crlat="betReceipt.continueButton"]'
    _total_stake = 'xpath=.//*[@data-crlat="betReceipt.totalStake"]'

    @property
    def success_message_text(self):
        return self._get_webelement_text(selector=self._success_bet_message, context=self._we, timeout=10)

    @property
    def failed_bet_data(self):
        return self._get_webelement_text(selector=self._failed_bet_receipt_data, timeout=3, context=self._we)

    @property
    def failed_message_text(self):
        return self._get_webelement_text(selector=self._failed_message, context=self._we)

    @property
    def bet_rules(self):
        return self._find_element_by_selector(selector=self._bet_rules).text

    @property
    def continue_button(self):
        return ButtonBase(selector=self._continue_btn)

    @property
    def total_stake(self):
        return Stake(selector=self._total_stake, context=self._we)
