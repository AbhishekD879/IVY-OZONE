from collections import OrderedDict

from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.markets.market_section_base import SwitcherMarketSection
from voltron.pages.shared.contents.base_contents.common_base_components.bet_button import BetButton


class Outcome(ComponentBase):
    _event_name = 'xpath=.//*[@data-crlat="oddsPrice"]'
    _bet_button = 'xpath=.//*[@data-crlat="betButton"]'

    @property
    def event_name(self):
        return self._get_webelement_text(selector=self._event_name, timeout=2)

    @property
    def bet_button(self):
        return BetButton(selector=self._bet_button, context=self._we)

    @property
    def name(self):
        return self.event_name


class OutcomeGroup(ComponentBase):
    _item = 'xpath=.//div[.//*[@data-crlat="betButton"]]'
    _list_item_type = Outcome
    _name = 'xpath=.//*[@data-crlat="oddsNames"]'

    @property
    def name(self):
        return self._get_webelement_text(selector=self._name)


class HandicapOutcomeGroup(OutcomeGroup):
    _item = 'xpath=.//*[@data-crlat="betButton"]'
    _list_item_type = BetButton

    @property
    def items_as_ordered_dict(self) -> OrderedDict:
        """
        Override method in parent class in order to have appropriate items names

        :return: Ordered Dict of items (str, BetButton)
        """
        items_we = self._find_elements_by_selector(selector=self._item, context=self._we)
        self._logger.debug(f'*** Found {len(items_we)} {self.__class__.__name__} - {self._list_item_type.__name__} items')
        items_ordered_dict = OrderedDict(
            zip(['Home', 'Tie', 'Away'], [self._list_item_type(web_element=item_we) for item_we in items_we]))
        return items_ordered_dict


class HandicapResultsEventTable(ComponentBase):
    _item = 'xpath=.//*[@data-crlat="oddsCard"]'
    _list_item_type = HandicapOutcomeGroup


class HandicapResultsMarket(SwitcherMarketSection):
    _outcomes = 'xpath=.//*[@data-crlat="containerInnerContent.table"]'
    _outcomes_table_type = HandicapResultsEventTable

    @property
    def outcomes(self):
        return self._outcomes_table_type(self._outcomes, context=self._we)
