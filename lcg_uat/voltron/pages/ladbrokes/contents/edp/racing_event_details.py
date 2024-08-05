from voltron.pages.shared.contents.edp.racing_event_details import RacingEventDetails, RacingEDPTabContent, \
    EventTabsMenuItem, EventMarketsList, EventTabsMenu, RaceDetailsContainer
from voltron.pages.ladbrokes.components.racing_post_verdict_overlay import RacePostVerdictOverlayDesktop
from voltron.pages.ladbrokes.components.racing_post_verdict_overlay import RacePostVerdictOverlay
from voltron.pages.shared.contents.edp.racing_event_details_desktop import MeetingsListDesktop
from voltron.utils.waiters import wait_for_result


class EventTabsMenuItemLadbrokes(EventTabsMenuItem):
    _item_name = 'xpath=.//*[@data-crlat="switcher.name"]'


class EventTabsMenuLadbrokes(EventTabsMenu):
    _list_item_type = EventTabsMenuItemLadbrokes


class EventMarketsListLadbrokes(EventMarketsList):
    _market_tabs_list = 'xpath=.//*[@data-crlat="switchers"]'
    _market_tabs_list_type = EventTabsMenuLadbrokes
    _uk_tote_section = 'xpath=.//*[@data-crlat="UKToteEvent"]'
    _add_to_betslip_button = 'xpath=.//*[@data-crlat="addToBetslipButton"]'
    _market_name = 'xpath=.//*[@data-crlat="headerTitle.centerMessage"]'
    _market_outcome = 'xpath=.//*[@data-crlat="marketOutcomes"]'

    @property
    def market_name(self):
        return self._find_element_by_selector(selector=self._market_name, timeout=1)

    def is_expanded(self, timeout=1, expected_result=True):
        result = wait_for_result(lambda: 'is-expanded' in self._find_element_by_selector(selector=self._market_outcome,
                                                                                         timeout=0).get_attribute('class'),
                                 name=f'"{self.__class__.__name__}" Specials list to expand',
                                 expected_result=expected_result,
                                 timeout=timeout)
        self._logger.debug(f'*** "{self.__class__.__name__}" Specials Market list: expanded status is "{result}"')
        return result


class RaceDetailsContainerLadbrokes(RaceDetailsContainer):
    _race_time = 'xpath=.//*[@data-crlat="specialsDate"] | .//*[@data-crlat="value"]'
    _event_title_time = 'xpath=.//*[@data-crlat="eventTitleTime"] | .//*[@data-crlat="specialsDate"]'
    _event_title_name = 'xpath=.//*[@data-crlat="eventTitleName"]'

    @property
    def event_title_time(self):
        return self._get_webelement_text(selector=self._event_title_time, context=self._we, timeout=2)

    @property
    def event_title_name(self):
        return self._get_webelement_text(selector=self._event_title_name, context=self._we)

    @property
    def event_title(self):
        return f'{self.event_title_time} {self.event_title_name}'

    @property
    def race_time(self):
        return self._get_webelement_text(selector=self._race_time, context=self._we)


class RacingEDPTabContentLadbrokes(RacingEDPTabContent):
    _event_markets_list_type = EventMarketsListLadbrokes

    @property
    def race_details(self):
        return RaceDetailsContainerLadbrokes(selector=self._race_details_container, context=self._we)


class RacingEDPTabContentLadbrokesDesktop(RacingEDPTabContentLadbrokes):
    _event_markets_list_type = EventMarketsList


class RacingEventDetailsLadbrokes(RacingEventDetails):
    _tab_content_type = RacingEDPTabContentLadbrokes
    _event_title_time = 'xpath=.//*[@data-crlat="eventTitleTime"]'
    _event_title_name = 'xpath=.//*[@data-crlat="eventTitleName"]'
    _racing_post_verdict = 'xpath=.//*[@data-crlat="drawer.content"]'

    @property
    def event_title_time(self):
        return self._get_webelement_text(selector=self._event_title_time, context=self._we, timeout=2)

    @property
    def event_title_name(self):
        return self._get_webelement_text(selector=self._event_title_name, context=self._we)

    @property
    def event_title(self):
        return f'{self.event_title_time} {self.event_title_name}'

    @property
    def racing_post_verdict(self):
        return RacePostVerdictOverlay(selector=self._racing_post_verdict)


class RacingEventDetailsLadbrokesDesktop(RacingEventDetailsLadbrokes):
    _tab_content_type = RacingEDPTabContentLadbrokesDesktop
    _meetings_list_type = MeetingsListDesktop
    _racing_post_verdict = 'xpath=.//*[@data-crlat="racingPostContainer"]//accordion'

    @property
    def racing_post_verdict(self):
        racing_post_verdict = self._find_element_by_selector(selector=self._racing_post_verdict, context=self._we,
                                                             timeout=2)
        return RacePostVerdictOverlayDesktop(web_element=racing_post_verdict) if racing_post_verdict else None
