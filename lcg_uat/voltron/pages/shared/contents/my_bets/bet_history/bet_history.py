from voltron.pages.shared.components.accordions_container import Accordion
from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.date_picker import DatePicker
from voltron.pages.shared.components.primitives.text_labels import TextBase
from voltron.pages.shared.contents.my_bets.bet_history.jackpot_pool_type import BetHistoryJackpotTotePool
from voltron.pages.shared.contents.my_bets.bet_history.lotto_bet_type import BetHistoryLottoBet
from voltron.pages.shared.contents.my_bets.bet_history.multiple_legs_tote_pool_type import BetHistoryMultipleTotePool
from voltron.pages.shared.contents.my_bets.bet_history.one_leg_tote_pool_type import BetHistoryOneLegTotePool
from voltron.pages.shared.contents.my_bets.bet_history.regular_bet_type import BetHistoryOpenBet
from voltron.pages.shared.contents.my_bets.bet_history.tote_bet_type import BetHistoryTotePoolBetCard
from voltron.pages.shared.contents.my_bets.open_bets.open_bets import OpenBetsEventsList
from voltron.pages.shared.contents.my_bets.open_bets.open_bets import OpenBetsTabContent
from voltron.pages.shared.contents.my_bets.open_bets.open_bets import OpenBets
from voltron.utils.waiters import wait_for_result


class SettledBetsTextBase(TextBase):

    @property
    def name(self):
        return self.label


class SettledBetsStakesReturnsSection(ComponentBase):
    _item = 'xpath=.//*[@data-crlat="summaryCol"]'
    _list_item_type = SettledBetsTextBase


class SettledBetsSummary(ComponentBase):
    _summary_label = 'xpath=.//*[@data-crlat="summaryHeaderLabel"]'
    _show_all_button = 'xpath=.//*[@data-crlat="showAllButton"]'
    _result_value = 'xpath=.//*[@data-crlat="resultValue"]'
    _stakes_returns_section = 'xpath=.//*[@data-crlat="stakesReturnsSection"]'
    _stakes_returns_section_type = SettledBetsStakesReturnsSection

    @property
    def name(self):
        return ''

    @property
    def summary(self):
        return self._get_webelement_text(selector=self._summary_label)

    @property
    def show_all_button(self):
        return ComponentBase(selector=self._show_all_button)

    @property
    def result_value(self):
        return self._get_webelement_text(selector=self._result_value)

    @property
    def stakes_returns_section(self):
        return self._stakes_returns_section_type(selector=self._stakes_returns_section)


class BetHistorySettledBets(Accordion):
    _item = 'xpath=.//*[@data-crlat="summarySection"]'
    _list_item_type = SettledBetsSummary
    _fade_out_overlay = True
    _verify_spinner = True


class BetHistoryEventsList(OpenBetsEventsList):
    _date_picker = 'xpath=.//*[@class="datepickers-section"] | .//*[@data-crlat="datePickersSection"] | .//*[@class="datepickers-section ng-star-inserted"]'
    _date_picker_type = DatePicker
    _no_bets_message = 'xpath=.//*[@data-crlat="textMsg"]'
    _settled_bets = 'xpath=.//*[@data-crlat="accordion"]'
    _regular_bet_type = BetHistoryOpenBet
    _lotto_bet_type = BetHistoryLottoBet
    _tote_bet_type = BetHistoryTotePoolBetCard

    _multiple_legs_tote_pool_type = BetHistoryMultipleTotePool
    _jackpot_pool_type = BetHistoryJackpotTotePool
    _one_leg_tote_pool_type = BetHistoryOneLegTotePool

    @property
    def settled_bets(self):
        return BetHistorySettledBets(selector=self._settled_bets, context=self._we, timeout=3)

    @property
    def no_bets_message(self):
        return self._get_webelement_text(selector=self._no_bets_message, timeout=3)

    @property
    def date_picker(self):
        return DatePicker(selector=self._date_picker, context=self._we)

    def has_date_picker(self, expected_result=True, timeout=1):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._date_picker,
                                                                      timeout=0),
                               expected_result=expected_result,
                               timeout=timeout,
                               name=f'Datepicker shown status to be {expected_result}')


class BetHistoryTabContent(OpenBetsTabContent):
    _accordions_list_type = BetHistoryEventsList


class BetHistory(OpenBets):
    _url_pattern = r'^http[s]?:\/\/.+\/(bet-history|account-history)'
    _tab_content_type = BetHistoryTabContent


class BetHistoryDesktop(Accordion, BetHistory):
    _url_pattern = r'^http[s]?:\/\/.+\/'
    _tab_content = 'xpath=.//*[@data-crlat="bsTabsContainer"]'
