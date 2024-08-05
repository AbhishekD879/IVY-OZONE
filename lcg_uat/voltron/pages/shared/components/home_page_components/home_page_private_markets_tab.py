from voltron.pages.shared.components.primitives.text_labels import LinkBase
from voltron.pages.shared.contents.base_contents.common_base_components.accordions_list import AccordionsList
from voltron.pages.shared.contents.base_contents.common_base_components.tab_content import TabContent
from voltron.pages.shared.components.markets.match_result_market import Outcome
from voltron.pages.shared.components.markets.market_section_base import MarketSection


class PrivateMarketsOutcomes(Outcome):
    _outcome_name = 'xpath=.//*[@data-crlat="outcome.name"]'
    _private_market_icon = 'xpath=//*[@data-crlat="privateMarketIcon"]'

    @property
    def private_market_icon(self):
        return self._find_element_by_selector(self._private_market_icon, context=self._we)


class PrivateMarkets(MarketSection):
    _item = 'xpath=.//*[@data-crlat="oddsCard"]'
    _list_item_type = PrivateMarketsOutcomes
    _private_market_icon = 'xpath=.//*[@data-crlat="privateMarketIcon"]'
    _name = 'xpath=.//*[@data-crlat="headerTitle.centerMessage"]'

    @property
    def name(self):
        return self._wait_for_not_empty_web_element_text(selector=self._name, context=self._we, timeout=3)


class PrivateMarketsAccordionsList(AccordionsList):
    _list_item_type = PrivateMarkets


class PrivateMarketsTabContent(TabContent):
    _url_pattern = r'^http[s]?:\/\/.+\/(home\/private-markets)'
    _accordions_list_type = PrivateMarketsAccordionsList
    _terms_and_conditions = 'xpath=.//*[@data-crlat="termsAndConditions"]'

    @property
    def terms_and_conditions(self):
        return LinkBase(self._terms_and_conditions, context=self._we)


class PrivateMarketsTabContentDesktop(PrivateMarketsTabContent):

    @property
    def accordions_list(self):
        return self._accordions_list_type(web_element=self._we, selector=self._selector, context=self._context)
