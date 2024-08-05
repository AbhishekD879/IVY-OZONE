from voltron.pages.shared.contents.base_contents.common_base_components.bet_button import BetButton
from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.markets.market_section_base import SwitcherMarketSection
from voltron.utils.exceptions.voltron_exception import VoltronException


class Outcome(ComponentBase):
    _outcome_name = 'xpath=.//*[@data-crlat="outcomeEntity.name" or @data-crlat="oddsNames" or @data-crlat="outcome.name"] | .//*[@data-crlat="outcome.alphabetName"]'
    _output_price_button = 'xpath=.//*[@data-crlat="betButton"]'
    _was_price = 'xpath=.//*[@class="was-price"]'

    @property
    def was_price(self):
        return self._get_webelement_text(selector=self._was_price)

    @property
    def outcome_name(self):
        return self._get_webelement_text(selector=self._outcome_name)

    @property
    def name(self):
        return self.outcome_name

    @property
    def output_price(self):
        we_text = self._get_webelement_text(selector=self._output_price_button)
        if we_text != '':
            return we_text
        else:
            return VoltronException(message='Output price on btn is not found')

    @property
    def bet_button(self):
        return BetButton(selector=self._output_price_button, context=self._we)


class MarketOutcomesList(ComponentBase):
    _item = 'xpath=.//*[@data-crlat="oddsCard"]'
    _list_item_type = Outcome
    _terms = 'xpath=.//*[@data-crlat="terms"]'

    @property
    def has_terms(self):
        return self._find_element_by_selector(selector=self._terms, timeout=0) is not None

    @property
    def terms_text(self):
        return self._get_webelement_text(selector=self._terms)


class MatchResultMarket(SwitcherMarketSection):
    _outcomes_list = 'xpath=.//*[@data-crlat="containerContent"] | .//accordion-body'
    _outcomes_list_type = MarketOutcomesList

    @property
    def outcomes(self):
        return self._outcomes_list_type(selector=self._outcomes_list, context=self._we)
