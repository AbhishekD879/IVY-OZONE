from collections import OrderedDict

from voltron.pages.shared.components.markets.handicap_results_market import HandicapResultsEventTable
from voltron.pages.shared.components.markets.handicap_results_market import HandicapResultsMarket
from voltron.pages.shared.components.markets.handicap_results_market import OutcomeGroup
from voltron.pages.shared.contents.base_contents.common_base_components.bet_button import BetButton


class OverUnderOutcomeGroup(OutcomeGroup):
    _item = 'xpath=.//*[@data-crlat="betButton"]'
    _list_item_type = BetButton

    @property
    def items_as_ordered_dict(self) -> OrderedDict:
        items_we = self._find_elements_by_selector(selector=self._item, context=self._we)
        self._logger.debug(f'*** Found {len(items_we)} {self.__class__.__name__} - {self._list_item_type.__name__} items')
        items_ordered_dict = OrderedDict(zip(['Over', 'Under'], [self._list_item_type(web_element=item_we) for item_we in items_we]))
        return items_ordered_dict


class OutcomesTable(HandicapResultsEventTable):
    _list_item_type = OverUnderOutcomeGroup
    _columns = 'xpath=.//*[@data-crlat="oddsHeader"]'
    _item = 'xpath=.//*[@data-crlat="oddsCard"]'

    @property
    def columns(self):
        column_names = []
        columns = self._find_elements_by_selector(selector=self._columns)
        for column in columns:
            column_names.append(column.text)
        return column_names


class OverUnderTotalGoalsMarket(HandicapResultsMarket):
    _outcomes_table_type = OutcomesTable
    _outcomes_table = 'xpath=.//*[@data-crlat="containerInnerContent.table"]'

    @property
    def outcomes_table(self):
        return self._outcomes_table_type(self._outcomes_table, context=self._we)
