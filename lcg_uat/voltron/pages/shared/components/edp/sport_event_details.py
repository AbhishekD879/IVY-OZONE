import re
from collections import OrderedDict

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException

from voltron.pages.shared import get_cms_config
from voltron.pages.shared import get_driver
from voltron.pages.shared.components.markets.correct_score_market import CorrectScoreMarket
from voltron.pages.shared.components.markets.double_chance_market import DoubleChanceMarket
from voltron.pages.shared.components.markets.handicap_results_market import HandicapResultsMarket
from voltron.pages.shared.components.markets.match_result_market import MatchResultMarket
from voltron.pages.shared.components.markets.other_goalscorer_market import OtherGoalscorerMarket
from voltron.pages.shared.components.markets.outright_market import OutrightMarket
from voltron.pages.shared.components.markets.over_under_home_away_total_goals_market import \
    OverUnderHomeAwayTeamTotalGoalsMarket
from voltron.pages.shared.components.markets.over_under_total_goals_market import OverUnderTotalGoalsMarket
from voltron.pages.shared.components.markets.popular_goalscorer_market import PopularGoalscorerMarket
from voltron.pages.shared.components.markets.scorecast_market import ScorecastMarket
from voltron.pages.shared.components.markets.your_call_specials_market import YourCallSpecialsMarket
from voltron.pages.shared.contents.base_contents.common_base_components.accordions_list import AccordionsList
from voltron.pages.shared.contents.base_contents.common_base_components.tab_content import TabContent
from voltron.pages.shared.contents.base_contents.common_base_components.tabs_menu import TabsMenu
from voltron.pages.shared.contents.base_contents.common_base_components.tabs_menu import TabsMenuItem
from voltron.pages.shared.contents.my_bets.cashout import Bet
from voltron.pages.shared.contents.my_bets.cashout import BetLeg
from voltron.pages.shared.contents.my_bets.cashout import CashoutEventsList
from voltron.pages.shared.contents.my_bets.cashout import CashoutTabContent
from voltron.pages.shared.contents.your_call import SportsYourCallEventGroup
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.waiters import wait_for_result


class MarketTabItem(TabsMenuItem):
    # Pls do not merge here changes from lower branches
    _market_tab_name = 'xpath=.//*[@data-crlat="tab"]/span[not(contains(@class, "badge-new"))] | .//*[@data-crlat="buttonSwitch"]/span[not(contains(@class, "badge-new"))]'

    @property
    def name(self):
        we = self._find_element_by_selector(selector=self._market_tab_name)
        return self._we_text(we)

    def click(self):
        self.scroll_to_we()
        we = self._find_element_by_selector(selector=self._market_tab_name)
        self.perform_click(we)


class MarketTabsList(TabsMenu):
    _item = 'xpath=.//*[@data-crlat="tab.tpTabs"][.//*[@data-crlat="tab"]] | .//*[@data-crlat="buttonSwitch"]/parent::li'
    _list_item_type = MarketTabItem
    _selected_item = 'xpath=.//*[@data-crlat="tab.tpTabs" ' \
                     'and(contains(@class, "active") or contains(@class, "selected"))] | .//*[@data-crlat="buttonSwitch" and(contains(@class, "active"))]/parent::li'


class EventUserTabItem(MarketTabItem):
    _market_tab_name = 'xpath=.//*[@data-crlat="tab"] | .//*[@data-crlat="buttonSwitch"]'

    def wait_is_visible(self):
        wait_for_result(lambda: self._we.is_displayed(),
                        timeout=5,
                        expected_result=True,
                        name='Waiting for Event user tabs to be visible')

    @property
    def name(self):
        self.wait_is_visible()
        we = self._find_element_by_selector(selector=self._market_tab_name)
        if we:
            text = self._get_webelement_text(we=we)
            find = re.search(r'[^\d().]+', text)
            if find:
                return find.group(0).rstrip()
            else:
                raise VoltronException('Cannot get text for Tab')
        else:
            raise VoltronException('No element matching %s was found' % self._market_tab_name)


class EventUserTabsList(MarketTabsList):
    _list_item_type = EventUserTabItem


class MarketsSectionsList(AccordionsList):
    _item = 'xpath=.//*[@data-crlat="accordion" and not(contains(@class, "page-inner-container"))] ' \
            '| .//*[@data-crlat="accordion"][.//*[text()]]'  # w/a for Outrights page
    _list_item_type = None
    _default_market_sections_list_type = MatchResultMarket
    _match_result_market = MatchResultMarket
    _outright_market = OutrightMarket
    _correct_score_market = CorrectScoreMarket
    _scorecast_market = ScorecastMarket
    _handicap_results_market = HandicapResultsMarket
    _popular_goalscorer_market = PopularGoalscorerMarket
    _other_goalscorer_market = OtherGoalscorerMarket
    _your_call_specials_market = YourCallSpecialsMarket
    _sports_yourcall_event_group = SportsYourCallEventGroup
    _over_under_total_goals_market = OverUnderTotalGoalsMarket
    _double_chance_market = DoubleChanceMarket
    _over_under_home_away_total_goals_market = OverUnderHomeAwayTeamTotalGoalsMarket

    _accordions_list_type = {
        'MATCH RESULT': _match_result_market,
        'OUTRIGHT': _outright_market,
        'TO WIN': _outright_market,
        'CORRECT SCORE': _correct_score_market,
        'FIRST HALF CORRECT SCORE': _correct_score_market,
        'SECOND HALF CORRECT SCORE': _correct_score_market,
        'SCORECAST': _scorecast_market,
        'HANDICAP RESULTS': _handicap_results_market,
        'POPULAR GOALSCORER MARKETS': _popular_goalscorer_market,
        'OTHER GOALSCORER MARKETS': _other_goalscorer_market,
        '#YOURCALL SPECIALS FOOTBALL': _your_call_specials_market,
        '#YOURCALL': _sports_yourcall_event_group,
        'EXTRA-TIME RESULT': _match_result_market,
        'OVER/UNDER TOTAL GOALS': _over_under_total_goals_market,
        'OVER/UNDER GOALS': _over_under_home_away_total_goals_market,
        'DOUBLE CHANCE': _double_chance_market,
        'PROMOTION': _outright_market
    }
    # todo incorrect structure of market names Scorecast in block Correct Score
    _market_name = 'xpath=.//*[contains(@data-crlat, "headerTitle.leftMessage") or @data-crlat="headerTitle.centerMessage" or @data-crlat="headerTitle"]'

    def _get_market_type(self, section):
        self.scroll_to_we(section)
        market_name_orig = self._get_webelement_text(selector=self._market_name, context=section)
        market_name = market_name_orig.upper()

        if 'OVER/UNDER GOALS' in market_name:
            market_name = 'OVER/UNDER GOALS'

        if market_name in self._accordions_list_type:
            market_template = self._accordions_list_type[market_name]
        else:
            self._logger.warning(f'*** Type is not recognized by name "{market_name_orig}". Check if it is CMS configurable Yourcall')
            if market_name == self._get_your_call_market_name:
                market_template = self._sports_yourcall_event_group
            else:
                self._logger.warning('*** Type is not recognized by name "%s" suppose it is: "%s"'
                                     % (market_name_orig, self._default_market_sections_list_type.__name__))
                market_template = self._default_market_sections_list_type
        self._logger.debug('*** Recognized "%s" by name "%s"' % (market_template.__name__, market_name_orig))
        inner_section = self._find_element_by_selector(selector=self._item, context=section, timeout=0)
        if inner_section and market_name not in ['#YOURCALL SPECIALS FOOTBALL', '#YOURCALL']:
            section = inner_section
        if market_name in ['FEATURED', 'ODDS ON', 'EVENTS - 5/2', '5/2 - 10/1', '11/1 - 40/1', '50/1 +']:
            # This is added due to incorrect structure of markets in outright page.
            market_template = self._your_call_specials_market
            return market_name_orig, market_template(web_element=section)
        return market_name_orig, market_template(web_element=section)

    @property
    def _get_your_call_market_name(self):
        cms = get_cms_config()
        initial_data = cms.get_initial_data(cached=True)
        your_call_market = initial_data.get('YourCallMarket')
        if not your_call_market:
            your_call_market = cms.get_system_configuration_item('YourCallMarket')
        if your_call_market:
            football_yc_market_name = your_call_market.get('football')
            if football_yc_market_name:
                return football_yc_market_name.upper()

    @property
    def items_as_ordered_dict(self) -> OrderedDict:
        items_we = self._find_elements_by_selector(selector=self._item, context=self._we)
        self._logger.debug(f'*** Found {len(items_we)} {self.__class__.__name__} items')
        items_as_ordered_dict = OrderedDict()
        for item_we in items_we:
            market_name, market_type = self._get_market_type(section=item_we)
            if not (market_name == ''):
                items_as_ordered_dict.update({market_name: market_type}) if market_type else None
        return items_as_ordered_dict

    def get_items(self, **kwargs) -> OrderedDict:
        """
        Get limited number of items in container
        :param kwargs: number - number of items, name - market name
        :return: OrderedDict with item name: item web element
        """
        name = kwargs.get('name')
        number = kwargs.get('number')
        items_we = self._find_elements_by_selector(selector=self._item, context=self._we)
        items_ordered_dict = OrderedDict()
        search_scope = [item_we for item_we in items_we] if name else [item_we for item_we in items_we[:number]]
        for item_we in search_scope:
            market_name, market_type = self._get_market_type(section=item_we)
            if name and (market_name == name):
                items_ordered_dict.update({market_name: market_type})
                break
            else:
                items_ordered_dict.update({market_name: market_type}) if market_type else None
        return items_ordered_dict


class MyBetLeg(BetLeg):

    @property
    def name(self):
        return self.outcome_name


class MyBet(Bet):
    _list_item_type = MyBetLeg

    @property
    def name(self):
        return '%s - [%s]' % (self.bet_type, ', '.join(
            [bet_leg.outcome_name for (bet_leg_name, bet_leg) in self.items_as_ordered_dict.items()]))


class MyBetsCashoutEventsList(CashoutEventsList):
    _list_item_type = MyBet


class MyBetsTabContent(CashoutTabContent):
    _accordions_list_type = MyBetsCashoutEventsList

    def _wait_active(self, timeout=0):
        self._find_elements_by_selector(selector=self._accordions_list, context=get_driver())
        self._we = self._find_myself()
        try:
            self._find_element_by_selector(selector=self._accordions_list,
                                           bypass_exceptions=(NoSuchElementException,))
        except StaleElementReferenceException:
            self._we = self._find_myself()


class EventDetailsPageTabContent(TabContent):
    _accordions_list_type = MarketsSectionsList


class DesktopMarketsSectionsList(MarketsSectionsList):
    _item = 'xpath=.//*[@data-crlat="accordion"]'


class DesktopEventDetailsPageTabContent(EventDetailsPageTabContent):
    _accordions_list_type = DesktopMarketsSectionsList
