from voltron.pages.ladbrokes.components.five_a_side_tab_content import FiveASideTabContent
from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.breadcrumbs import Breadcrumbs
from voltron.pages.shared import get_driver, get_device_properties
from voltron.pages.shared.components.edp.default_title_bar import DefaultTitleBar
from voltron.pages.shared.components.edp.opta_scoreboard_title_bar import OptaScoreboardTitleBar
from voltron.pages.shared.components.edp.scoreboard_title_bar import ScoreTitleBar
from voltron.pages.shared.components.edp.sport_event_details import DesktopEventDetailsPageTabContent
from voltron.pages.shared.components.edp.sport_event_details import EventDetailsPageTabContent
from voltron.pages.shared.components.edp.sport_event_details import EventUserTabsList
from voltron.pages.shared.components.edp.sport_event_details import MarketTabsList
from voltron.pages.shared.components.edp.sport_event_details import MyBetsTabContent
from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.pages.shared.contents.base_content import BaseContent
from voltron.pages.shared.contents.base_content import BaseDesktopContent
from voltron.pages.shared.contents.competitions_league_page import CompetitionsMatchesTabContent
from voltron.pages.shared.contents.edp.byb_event_details import BYBEventDetailsTabContent, BYBEventDetailsTabMenu
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.helpers import get_active_selector
from voltron.utils.js_functions import get_shadow_root
from voltron.utils.waiters import wait_for_result


class EventDetails(BaseContent):
    _url_pattern = r'^http[s]?:\/\/.+\/[\w-]+\/[\w-]+\/[\w-]+\/[\w-]+\/[0-9]+(/[\w-]+)+(\/[\w-])?$'

    # todo: VOL-1619 Components: Implement Event Header (EDP) component
    # TODO: need to distinguish between fav icon of event and star icon in header
    _event_name = 'xpath=.//*[@data-crlat="eventEntity.name"]'  # TODO VOL-4887
    _live_now_label = 'xpath=.//*[@data-crlat="liveLabel"]'
    # favourite_icon = 'xpath=.//*[@data-crlat="eventEntity"]//*[@data-crlat="favouriteIcon"]'
    _favourite_icon = 'xpath=.//*[@class="football-favourites"]//*[@data-crlat="favouriteIcon"]'
    _freebet_icon = 'xpath=.//*[@data-crlat="showFreeBetsIcon"]//*[@data-crlat="freeBetIcon"]'
    _stream_link = 'xpath=.//*[@data-crlat="streamLink"]'

    _my_bets_section_list = 'tag=my-bets'
    _my_bets_sections_list_type = MyBetsTabContent
    _watch_live_icon = 'xpath=.//*[@data-crlat="liveStream"]'
    _watch_live = 'xpath=.//*[@data-crlat="watchLive"] | .//span[contains(text(),"Watch")]'
    _live_stream = 'xpath=.//div[@class="video-frame"]//iframe'
    _markets_tabs_list = 'xpath=.//*[not(contains(@class, "ng-hide"))]/*[@data-crlat="panel.tabs"] | .//*[@data-crlat="switchers"]'
    _markets_tabs_list_type = MarketTabsList

    _event_user_tabs = 'xpath=.//*[@data-crlat="userTabs" or contains(@class, "tabs-list")]'  # TODO data-crlat
    _event_user_tabs_list_type = EventUserTabsList
    _fade_out_overlay = True

    _scoreboard_bar = 'xpath=.//fallback-scoreboard[not(.//*[contains(@data-crlat, "defBar")])] | .//*[@data-crlat="sbBar"][not(.//*[contains(@data-crlat, "defBar")])]'

    _default_bar = 'xpath=.//*[@data-crlat="defBar"]'

    _opta_scoreboard_bar = 'tag=scoreboard-container'
    _opta_match_summary = 'tag=match-summary'

    _tab_content_default = EventDetailsPageTabContent
    _tab_content_bet_builder = BYBEventDetailsTabContent
    _tab_menu_byb = 'xpath=.//*[@class="byb-tabs-container"]'
    _tab_menu_bet_builder = BYBEventDetailsTabMenu
    _event_name_team_home = 'xpath=.//*[@data-crlat="eventEntity"]//span[@data-crlat="teamH"]'
    _event_name_team_away = 'xpath=.//*[@data-crlat="eventEntity"]//span[@data-crlat="teamA"]'

    _change_match_selector = 'xpath=.//*[@data-crlat="changeMatch"]'
    _change_match_section = 'xpath=.//*[@data-crlat="quickSwitchHolder"]'

    def has_markets_my_bets_tab(self, timeout=1, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._event_user_tabs,
                                                   timeout=0) is not None,
            name=f'Icon status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)

    @property
    def event_name_team_home(self):
        we = self._find_element_by_selector(selector=self._event_name_team_home, timeout=3)
        if we is not None:
            return self._get_webelement_text(we=we)
        else:
            raise VoltronException('No element matching "%s" was found' % self._event_name)

    @property
    def event_name_team_away(self):
        we = self._find_element_by_selector(selector=self._event_name_team_away, timeout=3)
        if we is not None:
            return self._get_webelement_text(we=we)
        else:
            raise VoltronException('No element matching "%s" was found' % self._event_name)

    _tab_content_5_a_side = FiveASideTabContent

    def _wait_active(self, timeout=0):
        wait_for_result(lambda: self._find_element_by_selector(selector=self._tab_content, context=get_driver(), timeout=0) is not None,
                        name='Event Details Page to load',
                        timeout=5)

    def _get_tabs(self):
        dict_ = {
            'default': self._tab_content_default,
            'build-your-bet': self._tab_content_bet_builder,
            '5-a-side': self._tab_content_5_a_side,
            'pitch': self._tab_content_5_a_side,
        }
        return dict_

    @property
    def tab_content(self):
        url_tokens = get_driver().current_url.split('/')
        tabs = self._get_tabs()
        try:
            tab_content_url = url_tokens[-1]
            tab_content_url = tab_content_url.split('?')[0] if '?automationtest=true' in tab_content_url else tab_content_url
            self._tab_content_type = tabs.get(tab_content_url, tabs.get('default'))
        except (KeyError, IndexError):
            pass
        self._logger.debug(f'*** Recognized Tab Content type: {self._tab_content_type.__name__}')
        return self._tab_content_type(selector=self._tab_content)

    @property
    def favourite_icon(self):
        return ButtonBase(selector=self._favourite_icon)

    def has_favourite_icon(self, timeout=1, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._favourite_icon,
                                                   timeout=0) is not None,
            name=f'Icon status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)

    @property
    def freebet_icon(self):
        return ButtonBase(selector=self._freebet_icon)

    @property
    def has_freebet_icon(self):
        return self._find_element_by_selector(selector=self._freebet_icon, timeout=1) is not None

    @property
    def event_name(self):
        we = self._find_element_by_selector(selector=self._event_name, timeout=3)
        if we is not None:
            return self._get_webelement_text(we=we)
        else:
            raise VoltronException('No element matching "%s" was found' % self._event_name)

    @property
    def is_live_now_event(self):
        return self._find_element_by_selector(selector=self._live_now_label, timeout=0) is not None

    def has_stream(self, expected_result=True, timeout=1) -> bool:
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._stream_link, timeout=0) is not None,
                               expected_result=expected_result,
                               timeout=timeout,
                               name=f'Stream presence status to be "{expected_result}"')

    @property
    def event_user_tabs_list(self):
        return self._event_user_tabs_list_type(self._event_user_tabs, context=self._we)

    @property
    def tabs_menu_byb(self):
        return self._tab_menu_bet_builder(self._tab_menu_byb, context=self._we)

    def has_event_user_tabs_list(self, expected_result=True, timeout=1):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._event_user_tabs, context=self._we) is not None,
            expected_result=expected_result,
            timeout=timeout,
            name=f'Event user tabs status to be "{expected_result}"')

    @property
    def has_watch_live_icon(self):
        we = self._find_element_by_selector(selector=self._watch_live_icon,
                                            context=self._we, timeout=0)
        return ComponentBase(web_element=we, timeout=0).is_displayed() if we else False

    @property
    def watch_live_button(self):
        return self._find_element_by_selector(selector=self._watch_live, timeout=5)

    @property
    def streaming(self):
        return self._find_element_by_selector(selector=self._live_stream, timeout=5)

    @property
    def markets_tabs_list(self):
        return self._markets_tabs_list_type(self._markets_tabs_list, context=self._we, timeout=5)

    def has_pills(self,expected_result=True,timeout=1):
        result = wait_for_result(
            lambda: self._find_element_by_selector(selector=self._markets_tabs_list, context=self._we, timeout=0),
            name=f'Event pills are "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)
        return result

    @property
    def my_bets(self):
        return self._my_bets_sections_list_type(selector=self._my_bets_section_list, context=self._we)

    def has_event_scoreboard_bar(self, expected_result=True, timeout=1):
        result = wait_for_result(
            lambda: self._find_element_by_selector(selector=self._scoreboard_bar, context=self._we, timeout=0),
            name=f'Event scoreboard bar to be expected "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)
        return result

    @property
    def scoreboard_title_bar(self):
        return ScoreTitleBar(selector=self._scoreboard_bar, context=self._we, timeout=5)

    @property
    def default_title_bar(self):
        return DefaultTitleBar(selector=self._default_bar, context=self._we, timeout=5)

    @property
    def change_match_selector(self):
        return ButtonBase(selector=self._change_match_selector, context=self._we)

    def has_change_match_selector(self, expected_result=True, timeout=1):
        result = wait_for_result(
            lambda: self._find_element_by_selector(selector=self._change_match_selector, context=self._we, timeout=0),
            name=f'Event scoreboard bar to be expected "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)
        return result


    @property
    def change_match_section(self):
        return CompetitionsMatchesTabContent(selector=self._change_match_section, context=self._we)

    @property
    def opta_scoreboard_bar(self):
        we = self._find_element_by_selector(selector=self._opta_scoreboard_bar)
        if not we:
            raise VoltronException(f'Opta scoreboard bar not found by xpath "{self._opta_scoreboard_bar}"')
        context = get_shadow_root(we)
        if not context:
            raise VoltronException(f'Shadow root for "{self._opta_scoreboard_bar}" not found in Opta scoreboard bar')
        match_summary = self._find_element_by_selector(selector=self._opta_match_summary, context=context)
        if not match_summary:
            raise VoltronException(f'Match summary not found in Opta scoreboard bar')
        match_summary_context = get_shadow_root(match_summary)
        if not match_summary_context:
            raise VoltronException(f'Shadow root for "{self._opta_match_summary}" not found in Opta scoreboard bar')
        return OptaScoreboardTitleBar(web_element=match_summary_context)

    @property
    def event_title_bar(self):
        selectors = [self._scoreboard_bar, self._default_bar, self._opta_scoreboard_bar]
        selector = get_active_selector(selectors=selectors, timeout=30)
        if selector == self._scoreboard_bar:
            return self.scoreboard_title_bar
        elif selector == self._default_bar:
            return self.default_title_bar
        elif selector == self._opta_scoreboard_bar:
            return self.opta_scoreboard_bar
        raise VoltronException(
            f'Can not recognize event title bar type. All selectors from "{selectors}" are not available')


class DesktopEventDetails(EventDetails, BaseDesktopContent):
    _tab_content_type = DesktopEventDetailsPageTabContent
    _default_bar = 'xpath=.//*[@data-crlat="topBar"]'
    _favourite_icon = 'xpath=.//*[@data-crlat="favouriteIcon"]'
    _watch_live = 'xpath=.//*[@data-crlat="watchLive"]'
    _freebet_icon = 'xpath=.//*[@data-crlat="showFreeBetsIcon"]'
    _breadcrumbs_type = Breadcrumbs
    _breadcrumbs = 'xpath=.//*[@data-crlat="breadcrumbsContainer"]'

    _tab_content_default = DesktopEventDetailsPageTabContent

    def _wait_active(self, timeout=0):
        wait_for_result(lambda: self._find_element_by_selector(selector=self._breadcrumbs, context=get_driver(), timeout=0) is not None,
                        name='Event Details Page to load',
                        timeout=5)

    @property
    def breadcrumbs(self):
        return self._breadcrumbs_type(selector=self._breadcrumbs, context=self._we)

    def has_watch_live_button(self, expected_result=True):
        result = wait_for_result(lambda: self._find_element_by_selector(selector=self._watch_live,
                                                                        context=self._we,
                                                                        timeout=0) and self._find_element_by_selector(selector=self._watch_live,
                                                                                                                      context=self._we,
                                                                                                                      timeout=0).is_displayed(),
                                 name='Watch live button to appear',
                                 expected_result=expected_result,
                                 timeout=5)
        return result
