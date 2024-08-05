from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.markets.handicap_results_market import Outcome
from voltron.pages.shared.components.markets.market_section_base import SwitcherMarketSection


class DoubleChanceOutcome(Outcome):
    _event_name = 'xpath=.//*[@data-crlat="outcome.alphabetName"]'


class DoubleChanceOutcomes(ComponentBase):
    _item = 'xpath=.//*[@data-crlat="oddsCard"]'
    _list_item_type = DoubleChanceOutcome


class DoubleChanceMarket(SwitcherMarketSection):
    _outcomes = 'xpath=.//*[@data-crlat="containerInnerContent"]'
    _outcomes_type = DoubleChanceOutcomes

    @property
    def outcomes(self):
        return self._outcomes_type(self._outcomes, context=self._we)
