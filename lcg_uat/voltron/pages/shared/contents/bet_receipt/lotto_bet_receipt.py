# -*- coding: utf-8 -*-
from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.pages.shared.components.content_header import HeaderLine
from voltron.pages.shared.contents.lotto import Lotto
from voltron.utils.waiters import wait_for_result


# class BetReceiptSectionsList(ComponentBase):
#     _done_button = 'xpath=.//*[@data-crlat="doneButton"]'
#     _name = 'xpath=.//*[@data-crlat="receipt.name"]'
#     _event_name = 'xpath=.//*[@data-crlat="eventName"]'
#     _bet_type = 'xpath=.//*[@data-crlat="betType"]'
#     _bet_selections = 'xpath=.//*[@data-crlat="betSelections"]'
#     _bet_odds = 'xpath=.//*[@data-crlat="betOdds"]'
#     _bet_stake = 'xpath=.//*[@data-crlat="betStake"]'
#     _total_stake = 'xpath=.//*[@data-crlat="totalStake"]//strong'
#     _potential_return = 'xpath=.//*[@data-crlat="potentialReturn"]'
#     _bet_placed = 'xpath=.//*[@data-crlat="betPlaced"]'
#
#     @property
#     def name(self):
#         return self._get_webelement_text(selector=self._name, timeout=1)
#
#     @property
#     def event_name(self):
#         return self._get_webelement_text(selector=self._event_name, timeout=1)
#
#     @property
#     def bet_type(self):
#         return self._get_webelement_text(selector=self._bet_type, timeout=1)
#
#     @property
#     def bet_selections(self):
#         return self._get_webelement_text(selector=self._bet_selections, timeout=1)
#
#     @property
#     def bet_odds(self):
#         return self._get_webelement_text(selector=self._bet_odds, timeout=1)
#
#     @property
#     def bet_stake(self):
#         return self._get_webelement_text(selector=self._bet_stake, timeout=1)
#
#     @property
#     def bet_stake_value(self):
#         text = self.strip_currency_sign(self._get_webelement_text(selector=self._bet_stake, timeout=1))
#         return float(text.split('x')[0])
#
#     @property
#     def total_stake(self):
#         return self.strip_currency_sign(self._get_webelement_text(selector=self._total_stake, timeout=1))
#
#     @property
#     def total_stake_currency(self):
#         return self.get_currency_sign(self._get_webelement_text(selector=self._total_stake, timeout=1))
#
#     @property
#     def potential_return(self):
#         return self.strip_currency_sign(self._get_webelement_text(selector=self._potential_return, timeout=1))
#
#     @property
#     def bet_placed(self):
#         return self._get_webelement_text(selector=self._bet_placed, timeout=1)
#
#     @property
#     def done_button(self):
#         return ButtonBase(selector=self._done_button, timeout=1)
#
#
# class LottoReceiptTabContent(ComponentBase):
#     _betreceipt_sections_list = 'tag=lotto-receipt'
#     _betreceipt_sections_list_type = BetReceiptSectionsList
#     _header_line = 'xpath=.//header[@data-crlat="topBar"]'
#     _header_line_type = HeaderLine
#
#     def _wait_section_list_to_refresh(self):
#         s = self._find_element_by_selector(selector=self._betreceipt_sections_list)
#         wait_for_result(lambda: s != self._find_element_by_selector(selector=self._betreceipt_sections_list),
#                         name='Section list on Lotto Receipt to refresh',
#                         timeout=2)
#
#     @property
#     def header_line(self):
#         return self._header_line_type(selector=self._header_line)
#
#     @property
#     def section_list(self):
#         self._wait_section_list_to_refresh()
#         return self._betreceipt_sections_list_type(selector=self._betreceipt_sections_list)
#
#     @property
#     def betreceipt_header_line(self):
#         return self.header_line
#
#
# class LottoBetReceipt(Lotto):
#     _tab_content_type = LottoReceiptTabContent
