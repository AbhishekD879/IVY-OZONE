from voltron.pages.ladbrokes.contents.edp.byb_event_details import LadbrokesBYBEventDetailsTabContent
from voltron.pages.shared.components.breadcrumbs import Breadcrumbs
from voltron.pages.shared.components.edp.sport_event_details import MarketsSectionsList, MarketTabItem
from voltron.pages.shared.components.luckydip import LuckyDip
from voltron.pages.shared.contents.base_content import BaseDesktopContent
from voltron.pages.shared.contents.edp.sport_event_details import EventDetails, EventDetailsPageTabContent, MarketTabsList
from voltron.pages.shared.components.markets.match_result_market import MatchResultMarket
from voltron.pages.shared.components.markets.outright_market import OutrightMarket
from voltron.pages.shared.components.markets.scorecast_market import ScorecastMarket
from voltron.pages.shared.components.markets.your_call_specials_market import YourCallSpecialsMarket
from voltron.pages.ladbrokes.components.markets.handicap_results_market import LadbrokesHandicapResultsMarket
from voltron.pages.shared.contents.your_call import SportsYourCallEventGroup
from voltron.pages.ladbrokes.components.markets.correct_score_market import LadbrokesCorrectScoreMarket
from voltron.pages.ladbrokes.components.markets.double_chance_market import LadbrokesDoubleChanceMarket
from voltron.pages.ladbrokes.components.markets.other_goalscorer_market import LadbrokesOtherGoalscorerMarket
from voltron.pages.ladbrokes.components.markets.over_under_total_goals_market import LadbrokesOverUnderTotalGoalsMarket, \
    LadbrokesOverUnderHomeAwayTeamTotalGoalsMarket
from voltron.pages.ladbrokes.components.markets.popular_goalscorer_market import LadbrokesPopularGoalscorerMarket
from voltron.pages.ladbrokes.components.markets.draw_no_bet import LadbrokesDrawNoBet
from voltron.pages.shared.contents.base_contents.common_base_components.tabs_menu import TabsMenuItem
from voltron.utils.waiters import wait_for_result


class LadbrokesMarketsSectionsList(MarketsSectionsList):
    _correct_score_market = LadbrokesCorrectScoreMarket
    _popular_goalscorer_market = LadbrokesPopularGoalscorerMarket
    _other_goalscorer_market = LadbrokesOtherGoalscorerMarket
    _over_under_total_goals_market = LadbrokesOverUnderTotalGoalsMarket
    _double_chance_market = LadbrokesDoubleChanceMarket
    _match_result_market = MatchResultMarket
    _outright_market = OutrightMarket
    _scorecast_market = ScorecastMarket
    _handicap_results_market = LadbrokesHandicapResultsMarket
    _your_call_specials_market = YourCallSpecialsMarket
    _sports_yourcall_event_group = SportsYourCallEventGroup
    _draw_no_bet = LadbrokesDrawNoBet
    _over_under_home_away_total_goals_market = LadbrokesOverUnderHomeAwayTeamTotalGoalsMarket
    _luckydip_market = LuckyDip

    _accordions_list_type = {
        'MATCH BETTING': _match_result_market,
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
        'DOUBLE CHANCE': _double_chance_market,
        'PROMOTION': _outright_market,
        'DRAW NO BET': _draw_no_bet,
        'OVER/UNDER GOALS': _over_under_home_away_total_goals_market,
        'LUCKY DIP': _luckydip_market
    }


class LadbrokesEventDetailsPageTabContent(EventDetailsPageTabContent):
    _accordions_list_type = LadbrokesMarketsSectionsList


class LadbrokesMarketTabItem(MarketTabItem):
    _market_tab_name = 'xpath=.//*[@data-crlat="tab"]/span[not(contains(@class, "badge-new"))]'

    def is_selected(self, expected_result=True, timeout=2, poll_interval=0.5, name=None):
        if not name:
            name = f'"{self.__class__.__name__}" selected status is: {expected_result}'
        return wait_for_result(lambda: 'active' in self._we.get_attribute('class'),
                               expected_result=expected_result,
                               timeout=timeout,
                               poll_interval=poll_interval,
                               name=name)


class LadbrokesMarketTabItemDesktop(TabsMenuItem):
    _item_name = 'xpath=.//*[@data-crlat="switcher.name"]'

    def is_selected(self, expected_result=True, timeout=2, poll_interval=0.5, name=None):
        if not name:
            name = f'"{self.__class__.__name__}" selected status is: {expected_result}'
        return wait_for_result(lambda: 'active' in self._we.get_attribute('class'),
                               expected_result=expected_result,
                               timeout=timeout,
                               poll_interval=poll_interval,
                               name=name)


class LadbrokesMarketTabsList(MarketTabsList):
    _list_item_type = LadbrokesMarketTabItem


class LadbrokesMarketTabsListDesktop(MarketTabsList):
    _item = 'xpath=.//*[@data-crlat="buttonSwitch"]'
    _list_item_type = LadbrokesMarketTabItemDesktop
    _selected_item = 'xpath=.//*[@data-crlat="buttonSwitch" and contains(@class, "active")]'


class EventDetailsLadbrokes(EventDetails):
    _event_name = 'xpath=.//*[@data-crlat="eventEntity.name"]'
    _markets_tabs_list_type = LadbrokesMarketTabsList
    _tab_content_default = LadbrokesEventDetailsPageTabContent
    _tab_content_bet_builder = LadbrokesBYBEventDetailsTabContent

    def _get_tabs(self):
        dict_ = {
            'default': self._tab_content_default,
            'bet-builder': self._tab_content_bet_builder,
            '5-a-side': self._tab_content_5_a_side,
            'pitch': self._tab_content_5_a_side,
        }
        return dict_

    @property
    def event_name(self):
        return self._get_webelement_text(selector=self._event_name,timeout=3)


class DesktopMarketsSectionsListLadbrokes(MarketsSectionsList):
    _item = 'xpath=.//accordion'


class DesktopEventDetailsPageTabContentLadbrokes(EventDetailsPageTabContent):
    _accordions_list_type = DesktopMarketsSectionsListLadbrokes


class DesktopEventDetailsLadbrokes(EventDetailsLadbrokes, BaseDesktopContent):
    _default_bar = 'xpath=.//*[@data-crlat="topBar"]'
    _favourite_icon = 'xpath=.//*[@data-crlat="favouriteIcon"]'
    _watch_live = 'xpath=.//*[@data-crlat="watchLive"]'

    _breadcrumbs_type = Breadcrumbs
    _breadcrumbs = 'xpath=.//*[@data-crlat="breadcrumbsContainer"]'
    _markets_tabs_list_type = LadbrokesMarketTabsListDesktop

    _tab_content_default = DesktopEventDetailsPageTabContentLadbrokes

    @property
    def breadcrumbs(self):
        return self._breadcrumbs_type(selector=self._breadcrumbs, context=self._we)

    def has_watch_live_button(self, expected_result=True, timeout=10):
        result = wait_for_result(lambda: self._find_element_by_selector(selector=self._watch_live, timeout=0) and self._find_element_by_selector(selector=self._watch_live, timeout=0).is_displayed(),
                                 name='Watch live button to appear',
                                 expected_result=expected_result,
                                 timeout=timeout)
        return result
