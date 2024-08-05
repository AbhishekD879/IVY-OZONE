from collections import OrderedDict

from voltron.pages.shared import get_driver
from voltron.pages.shared.components.accordions_container import Accordion
from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.contents.base_content import ComponentContent
from voltron.pages.shared.contents.bet_receipt.bet_receipt import BetReceipt
from voltron.pages.shared.contents.bet_receipt.bet_receipt import BetReceiptSection
from voltron.pages.shared.contents.bet_receipt.bet_receipt import BetReceiptSectionsList


class Event(ComponentContent):
    _name = 'xpath=.//*[@data-crlat="eventEntity.name"]'
    _outcome = 'xpath=.//*[@data-crlat="receiptData.eventEntity"]'

    @property
    def name(self):
        return self._get_webelement_text(selector=self._name)

    @property
    def outcome(self):
        return self._get_webelement_text(selector=self._outcome)


class JackpotBetReceiptSection(BetReceiptSection, Accordion):
    _item = 'xpath=.//*[@data-crlat="eventEntity"]'
    _list_item_type = Event

    @property
    def items_as_ordered_dict(self) -> OrderedDict:
        items_we = self._find_elements_by_selector(selector=self._item, context=get_driver())
        self._logger.debug(f'*** Found {len(items_we)} {self.__class__.__name__} - {self._list_item_type.__name__} items')
        items_ordered_dict = OrderedDict()
        for item_we in items_we:
            list_item = self._list_item_type(web_element=item_we)
            items_ordered_dict.update({list_item.name: list_item})
        return items_ordered_dict

    @property
    def name(self):
        return 'JackpotReceipt'

    @property
    def bet_type(self):
        elements = self._find_elements_by_selector(selector=self._section_header, context=get_driver())
        we = [we for we in elements if we.text != '']
        return we[0].text

    @property
    def selections_count(self):
        return self._get_webelement_text(selector=self._selections_count, context=get_driver())


class DetailsSection(ComponentBase):
    _receipt_name = 'xpath=.//*[@data-crlat="sb.footballJackpot"]'
    _receipt_lines = 'xpath=.//*[@data-crlat="receiptLines"]'
    _receipt_no = 'xpath=.//*[@data-crlat="labelReceiptNumber"]'
    _total_stake = 'xpath=.//*[@data-crlat="totalStake"]'
    _total_lines = 'xpath=.//*[@data-crlat="totalLines"]'

    @property
    def receipt_name(self):
        return self._find_element_by_selector(selector=self._receipt_name).text

    @property
    def receipt_lines(self):
        return self._find_element_by_selector(selector=self._receipt_lines).text

    @property
    def receipt_no(self):
        return self._find_element_by_selector(selector=self._receipt_no).text

    @property
    def total_stake(self):
        total_stake = self._find_element_by_selector(selector=self._total_stake).text
        return total_stake if total_stake else '0'

    @property
    def total_lines(self):
        total_lines = self._find_element_by_selector(selector=self._total_lines).text
        return total_lines if total_lines else '0'


class JackpotBetReceiptSectionsList(BetReceiptSectionsList):
    _item = 'xpath=.//*[@data-crlat="containerContent"]'
    _list_item_type = JackpotBetReceiptSection
    _details_section = 'xpath=.//*[@data-crlat="detailsInfo"]'
    _done_button = 'xpath=.//*[@data-crlat="buttonDone"]'

    @property
    def details_section(self):
        return DetailsSection(selector=self._details_section)

    @property
    def done_button(self):
        return ButtonBase(selector=self._done_button)


class FootballJackpotReceipt(BetReceipt):
    _url_pattern = r'^http[s]?:\/\/.+\/football-jackpot-receipt'
    _betreceipt_sections_list = 'xpath=.//*[@data-crlat="pageContainer" or @data-uat="pageContent"]'
    _betreceipt_sections_list_type = JackpotBetReceiptSectionsList

    _load_complete_pattern = 'xpath=.//*[@data-crlat="labelReceiptNumber"]'

    @property
    def bet_receipt_sections_list(self):
        self.wait_for_page_title('Football Jackpot Bet Receipt'.upper())
        return self._betreceipt_sections_list_type(selector=self._betreceipt_sections_list)
