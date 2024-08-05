from collections import OrderedDict
from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.markets.market_section_base import MarketSection
from voltron.pages.shared.components.markets.match_result_market import MarketOutcomesList


class Outright(ComponentBase):
    _outright_odd_name = 'xpath=.//*[@data-crlat="oddsNames"]'
    _outright_odd_button = 'xpath=.//*[@data-crlat="betButton"]'

    @property
    def name(self):
        return self._get_webelement_text(selector=self._outright_odd_name)
    @property
    def odds(self):
        return self._find_element_by_selector(selector=self._outright_odd_button)


class OutrightMarket(MarketSection):
    _outright_market = 'xpath=.//*[@data-crlat="accordion"]'
    _outright_market_type = MarketOutcomesList
    _item = 'xpath=.//*[@data-crlat="oddsCard"]'
    _list_item_type = Outright

    @property
    def outcomes(self):
        return self._outright_market_type(web_element=self._we, selector=self._selector)

    @property
    def items_as_ordered_dict(self) -> OrderedDict:
        items_we = self._find_elements_by_selector(selector=self._item,context=self._we,timeout=self._timeout)
        items_ordered_dict = OrderedDict()
        for item_we in items_we:
            list_item = self._list_item_type(web_element=item_we)
            items_ordered_dict.update({list_item.name: list_item})
        return items_ordered_dict
