from voltron.pages.shared.components.markets.market_section_base import MarketSection
from voltron.pages.shared.components.markets.match_result_market import Outcome
from voltron.pages.shared.contents.base_contents.common_base_components.accordions_list import AccordionsList
from voltron.pages.shared.contents.base_contents.common_base_components.event_group import EventGroup


class YourCallOutcome(Outcome):
    _outcome_name = 'xpath=.//*[@data-crlat="oddsNames"]'


class YourCallMarketSection(MarketSection):
    _item = 'xpath=.//*[@data-crlat="oddsCard"]'
    _list_item_type = YourCallOutcome

    @property
    def output_prices(self):
        output_prices = []
        bet_buttons = self._find_elements_by_selector(selector=self._add_to_betslip_btn, timeout=1)
        for bet_button in bet_buttons:
            output_prices.append(bet_button.text)
        return output_prices


class YourCallSpecialsMarket(MarketSection):
    _item = 'xpath=.//*[@data-crlat="accordion"]'
    _list_item_type = YourCallMarketSection
    _outcome_name = 'xpath=.//*[@data-crlat="oddsNames"]'

    @property
    def outcome_name(self):
        return self._get_webelement_text(selector=self._outcome_name)


class SportsYourCallOutcomes(Outcome):

    @property
    def event_name(self):
        return self._get_webelement_text(selector=self._outcome_name)

    @property
    def name(self):
        return self.event_name


class SportsYourCallEventSubGroup(EventGroup, MarketSection):
    _item = 'xpath=.//*[@data-crlat="oddsCard"]'
    _list_item_type = SportsYourCallOutcomes

    @property
    def event_name(self):
        return self.name

    @property
    def output_prices(self):
        output_prices = []
        bet_buttons = self._find_elements_by_selector(selector=self._add_to_betslip_btn, timeout=1)
        for bet_button in bet_buttons:
            output_prices.append(bet_button.text)
        return output_prices


class SportsYourCallEventGroup(AccordionsList, EventGroup):
    _list_item_type = SportsYourCallEventSubGroup
