from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

from voltron.pages.shared.components.markets.build_your_bet.byb_match_result_market import BYBMatchResultMarket, BYBOutcome
from voltron.pages.shared.components.markets.match_result_market import MarketOutcomesList
from voltron.utils.waiters import wait_for_result


class BYBDoubleChanceMarketOutcomesList(MarketOutcomesList):
    _item = 'xpath=.//*[@data-crlat="yourcall.selection"]'
    _list_item_type = BYBOutcome


class BYBDoubleChanceMarket(BYBMatchResultMarket):
    _outcomes_list = 'xpath=.//*[@data-crlat="yourcallMarket.type"]'
    # _output_price_button = 'xpath=.//*[@data-crlat="betButton"]'
    _outcomes_list_type = BYBDoubleChanceMarketOutcomesList
    _fade_out_overlay = True
    _verify_spinner = True

    def _wait_active(self, timeout=0):
        if self.is_expanded(timeout=1):
            wait_for_result(lambda: len(self.outcomes.items_as_ordered_dict) > 0,
                            timeout=2,
                            name=f'{self.__class__.__name__} - Bet buttons to be displayed',
                            bypass_exceptions=(NoSuchElementException, StaleElementReferenceException, AttributeError))
