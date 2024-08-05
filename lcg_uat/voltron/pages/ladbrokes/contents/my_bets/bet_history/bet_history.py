from voltron.pages.shared.components.accordions_container import Accordion
from voltron.pages.shared.contents.my_bets.bet_history.bet_history import BetHistory
from voltron.pages.shared.contents.my_bets.bet_history.bet_history import BetHistoryEventsList
from voltron.pages.shared.contents.my_bets.bet_history.bet_history import BetHistoryTabContent


class LadbrokesBetHistoryEventsList(BetHistoryEventsList):
    _settled_bets = 'xpath=//*[@data-crlat="summaryAccordion"] | .//*[@class="profit-loss-link"]/a | .//*[' \
                    '@data-crlat="profitLossLink"]/*[data-crlat="link"] '


class LadbrokesBetHistoryTabContent(BetHistoryTabContent):
    _accordions_list_type = LadbrokesBetHistoryEventsList


class LadbrokesBetHistory(BetHistory):
    _tab_content_type = LadbrokesBetHistoryTabContent


class LadbrokesBetHistoryDesktop(Accordion, LadbrokesBetHistory):
    _url_pattern = r'^http[s]?:\/\/.+\/'
    _tab_content = 'xpath=.//*[@data-crlat="slideContent.betHistory" or @data-crlat="slideContent.3"]/parent::*'
