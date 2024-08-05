from voltron.pages.shared.components.accordions_container import Accordion
from voltron.pages.shared.components.primitives.text_labels import LinkBase
from voltron.pages.shared.contents.my_bets.bet_history.bet_history import BetHistoryEventsList, BetHistoryTabContent, \
    BetHistory


class CoralBetHistoryEventsList(BetHistoryEventsList):
    _settled_bets = 'xpath=.//*[@class="profit-loss-link"]/a | .//*[@data-crlat="profitLossLink"]/*[data-crlat="link"]'

    @property
    def settled_bets(self):
        return LinkBase(selector=self._settled_bets, context=self._we, timeout=3)


class CoralBetHistoryTabContent(BetHistoryTabContent):
    _accordions_list_type = CoralBetHistoryEventsList


class CoralBetHistory(BetHistory):
    _header_line = 'xpath=.//*[@data-crlat="topBarBetslipOpenBets"]'
    _tab_content_type = CoralBetHistoryTabContent


class CoralBetHistoryDesktop(Accordion, CoralBetHistory):
    _url_pattern = '^http[s]?:\/\/.+\/'
    _tab_content = 'xpath=.//*[@data-crlat="slideContent.betHistory" or @data-crlat="slideContent.3"]/parent::*'
