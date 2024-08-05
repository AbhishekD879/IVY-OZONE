from collections import OrderedDict

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from voltron.pages.shared import get_driver

from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.breadcrumbs import Breadcrumbs
from voltron.pages.shared.components.edp.sport_event_details import EventUserTabsList, MyBetsTabContent
from voltron.pages.shared.components.primitives.buttons import ButtonBase, SpinnerButtonBase
from voltron.pages.shared.components.primitives.buttons import ImageIconBase
from voltron.pages.shared.components.primitives.text_labels import TextBase
from voltron.pages.shared.contents.base_content import BaseContent
from voltron.pages.shared.contents.base_contents.common_base_components.tab_content import TabContent
from voltron.pages.shared.contents.base_contents.common_base_components.tabs_menu import TabsMenuItem, TabsMenu
from voltron.pages.shared.contents.base_contents.racing_base_components.enhanced_races_specials import RacesSpecials
from voltron.pages.shared.contents.base_contents.racing_base_components.event_off_times import EventOffTimesList
from voltron.pages.shared.contents.base_contents.racing_base_components.media_area import VideoStreamArea
from voltron.pages.shared.contents.base_contents.racing_base_components.media_area import WatchFreeArea
from voltron.pages.shared.contents.base_contents.racing_base_components.media_area import WatchFreeLink
from voltron.pages.shared.contents.base_contents.racing_base_components.meeting_selector import MeetingSelector
from voltron.pages.shared.contents.base_contents.racing_base_components.meeting_selector import MeetingsList
from voltron.pages.shared.contents.edp.racing_edp_market_section import RacingMarketSection
from voltron.pages.shared.contents.edp.racing_edp_market_section import SummaryText
from voltron.pages.shared.contents.edp.racing_uk_tote_edp_market_section import UKToteSection
from voltron.pages.shared.contents.edp.sport_event_details import EventDetails
from voltron.pages.shared.contents.my_stable.my_stable_page import EditStable
from voltron.utils.waiters import wait_for_result
from voltron.pages.shared.components.primitives.buttons import IconBase
from voltron.pages.shared.contents.edp.racing_edp_market_section import Outcome as RacingDetails
from voltron.pages.shared.contents.base_contents.racing_base_components.each_way_terms import EachWayTerms
from voltron.pages.shared.components.racing_post_verdict_overlay import RacePostVerdictOverlay


class EventTabsMenuItem(TabsMenuItem):
    _item_name = 'xpath=.//*[@data-crlat="tab"]'


class EventTabsMenu(TabsMenu):
    _list_item_type = EventTabsMenuItem


class EventMarketsList(ComponentBase):
    _item = 'xpath=.//*[@data-crlat="marketOutcomes"]'  # ToDo: This should be tab content actually, VOL-2428
    _market_tabs_list = 'xpath=.//*[@data-crlat="panel.tabs"]'
    _market_tabs_list_type = EventTabsMenu
    _uk_tote_section = 'xpath=.//*[@data-crlat="UKToteEvent"]'
    _add_to_betslip_button = 'xpath=.//*[@data-crlat="addToBetslipButton"]'

    def _wait_active(self, timeout=0):
        self._we = self._find_myself()
        wait_for_result(lambda: self.items_as_ordered_dict,
                        name=f'Waiting while tabs are loading',
                        timeout=3)

    @property
    def market_tabs_list(self):
        return self._market_tabs_list_type(selector=self._market_tabs_list, context=self._we)

    @property
    def current_market_tab_name(self):
        if self._find_element_by_selector(selector=self._market_tabs_list, timeout=0):
            return self.market_tabs_list.current
        else:
            self._logger.warning('*** Cannot find Market Tabs, suppose current event is Antepost event')
            return 'Antepost'

    def has_market_outcomes(self, tab_name, expected_result=True, timeout=5):
        if tab_name != self.current_market_tab_name:
            self.market_tabs_list.open_tab(tab_name)

        result = wait_for_result(lambda: self._find_element_by_selector(selector=self._item, timeout=0),
                                 timeout=timeout,
                                 expected_result=expected_result,
                                 name='Market tab to have outcomes')
        return result

    @property
    def _list_item_type(self):
        is_uk_tote = self._find_element_by_selector(selector=self._uk_tote_section, timeout=0)
        if is_uk_tote:
            return UKToteSection
        return RacingMarketSection

    @property
    def items_as_ordered_dict(self) -> OrderedDict:
        items_we = wait_for_result(lambda: self._find_elements_by_selector(selector=self._item, timeout=0),
                                   name='Racing EDP markets are loaded',
                                   timeout=10)
        self._logger.debug(
            f'*** Found {len(items_we)} {self.__class__.__name__} - {self._list_item_type.__name__} items')
        items_ordered_dict = OrderedDict(
            [
                (self.current_market_tab_name,
                 self._list_item_type(web_element=item_we)) for item_we in items_we
            ]
        )
        return items_ordered_dict

    @property
    def add_to_betslip_button(self):
        return ButtonBase(selector=self._add_to_betslip_button, context=self._we)


class SubHeader(ComponentBase):
    _meeting_name = 'xpath=.//*[@data-crlat="topBarTitle"]'
    _event_time = 'xpath=.//*[@data-crlat="eventTime"]'
    _meeting_selector = 'xpath=.//*[@data-crlat="meetingSelector"]'
    _meeting_selector_type = MeetingSelector

    @property
    def meeting_name(self):
        return self._get_webelement_text(selector=self._meeting_name, timeout=2)

    @property
    def event_time(self):
        return self._get_webelement_text(selector=self._event_time, timeout=1)

    def has_meeting_selector(self, timeout=1, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._meeting_selector,
                                                   timeout=0) is not None,
            name=f'Button status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)

    @property
    def meeting_selector(self):
        return self._meeting_selector_type(selector=self._meeting_selector)


class SilkIcon(IconBase):
    @property
    def name(self):
        return self.get_attribute('class')


class PostInfo(ComponentBase):
    _antepost_title = 'xpath=.//*[@data-crlat="antepost.label"]'
    _show_summary_btn = 'xpath=.//*[@data-crlat="racingPost.showSummary"]'
    _summary_text = 'xpath=.//*[@data-crlat="verdictInfo"]'
    _logo_icon = 'xpath=.//*[@data-crlat="racingPost.logo"]'
    _item = 'xpath=.//*[@data-crlat="imageSilk" or @data-crlat="gh-silk"]'
    _list_item_type = SilkIcon

    def has_summary_button(self, timeout=1, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._show_summary_btn,
                                                   timeout=0) is not None,
            name=f'Button status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)

    @property
    def show_summary_button(self):
        return ButtonBase(selector=self._show_summary_btn, context=self._we)

    @property
    def summary_text(self):
        return SummaryText(selector=self._summary_text, context=self._we)

    def has_logo_icon(self, timeout=1, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._logo_icon,
                                                   timeout=0) is not None,
            name=f'Logo status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)

    @property
    def logo_icon(self):
        return ImageIconBase(selector=self._logo_icon, context=self._we, timeout=1)

    @property
    def antepost_title(self):
        return self._get_webelement_text(selector=self._antepost_title)


class SortingToggleItem(ComponentBase):
    _name = 'xpath=.//*[@data-crlat="item-name"]'

    @property
    def name(self):
        return self._get_webelement_text(selector=self._name, context=self._we)


class SortingToggleSelector(ComponentBase):
    _list_item_type = SortingToggleItem
    _item = 'xpath=.//*[@data-crlat="item"]'


class SortingToggle(ComponentBase):
    _selected_option = 'xpath=.//*[@data-crlat="selected-option"]'
    _sort_type_selector = 'xpath=.//*[@data-crlat="sort-by-selector"]'

    @property
    def selected_option(self):
        return self._get_webelement_text(selector=self._selected_option)

    def open(self):
        ComponentBase(selector=self._sort_type_selector).click()


class RaceDetailsContainer(ComponentBase):
    _event_title = 'xpath=.//*[@data-crlat="eventTitle"]'
    _distance = 'xpath=.//*[@data-crlat="raceDistance"]'
    _going = 'xpath=.//*[@data-crlat="raceGoing"]'
    _countdown_container = 'xpath=.//*[@data-crlat="raceCountdown"]'
    _race_title = 'xpath=..//*[@data-crlat="eventTitle"] | .//*[@class="event-header"]'
    _race_type = 'xpath=.//*[@data-crlat="raceType"]'

    @property
    def event_title(self):
        return self._get_webelement_text(selector=self._event_title, context=self._we).replace('\n', " ")

    @property
    def race_going(self):
        return TextBase(selector=self._going, context=self._we)

    @property
    def race_distance(self):
        return TextBase(selector=self._distance, context=self._we)

    def has_race_distance(self, timeout=1, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._distance,
                                                   timeout=0) is not None,
            name=f'Button status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)

    def has_race_going(self, timeout=1, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._going,
                                                   timeout=0) is not None,
            name=f'Race going presence to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)

    def has_race_title(self, timeout=1, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._race_title,
                                                   timeout=0) is not None,
            name=f'Race title presence to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)

    def has_race_type(self, timeout=1, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._race_type,
                                                   timeout=0) is not None,
            name=f'Race type presence to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)

    @property
    def race_title(self):
        return TextBase(selector=self._race_title, context=self._we)

    @property
    def race_type(self):
        return TextBase(selector=self._race_type, context=self._we)

    @property
    def countdown_timer(self):
        return TextBase(selector=self._countdown_container, context=self._we)

    def has_countdown_timer(self, timeout=2, expected=True):
        result = wait_for_result(
            lambda: self._find_element_by_selector(selector=self._countdown_container, timeout=0),
            name=f'Countdown timer to be displayed',
            expected_result=expected,
            timeout=timeout)
        return result


class RacingEDPTabContent(TabContent):
    _race_details_container = 'xpath=.//*[@data-crlat="raceDetailsContainer"]'
    _post_info_container = 'xpath=.//racing-post-pick/*[@data-crlat="racingPostContainer"] | .//*[@class="terms-block"] | .//*[@data-crlat="racingPostContainer"]'
    _event_off_times_list = 'xpath=.//*[@data-crlat="eventTimePanel.tabs"]'
    _sorting_toggle = 'xpath=.//*[@data-crlat="sortingContainer"] | .//*[@data-crlat="sort-by-selector"]'
    _event_off_times_list_type = EventOffTimesList
    _video_stream_button = 'xpath=.//*[@data-crlat="buttonPlayStream"]'
    _event_markets_list = 'xpath=.//*[@data-crlat="eventTopContainer"]'
    _event_markets_list_type = EventMarketsList
    _watch_free_button = 'xpath=.//*[@data-crlat="buttonWatchFree"]'
    _watch_free_area = 'xpath=.//*[@data-crlat="iframeWatchFree"]'
    _video_stream_area = 'xpath=.//*[@data-crlat="eventVideoStreamArea"]'
    _watch_free_legend = 'xpath=.//*[@data-crlat="linkWatchFreeLegend"]'
    _video_stream_error = 'xpath=.//*[@data-crlat="videoStreamErrorMessage" and not(contains(@class, "ng-hide"))]'
    _sorting_selector = 'xpath=.//*[@data-crlat="sortSelector"]'
    _specials_carousel = 'xpath=.//*[@data-crlat="race.enhancedRacesCarousel"]'
    _live_commentary_link = 'xpath=.//*[@data-crlat="buttonLiveCommentary"]'
    _microphone_icon = 'xpath=.//*[@class="btn-icon live-commentary-icon"]'
    _specials_carousel_type = RacesSpecials
    _tooltip_container = 'xpath=.//*[contains(@class, "tooltip-container")]'

    @property
    def has_tooltip_container(self):
        return self._find_element_by_selector(selector=self._tooltip_container, timeout=2) is not None

    _additional_markets_tooltip = 'xpath=.//*[contains(@class, "tooltip tooltip-container")]'

    @property
    def additional_markets_tooltip(self):
        return self._find_element_by_selector(selector=self._additional_markets_tooltip, timeout=0)

    @property
    def has_additional_markets_tooltip(self, timeout=2, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._additional_markets_tooltip,
                                                   timeout=0) is not None,
            name=f'{self.__class__.__name__} – Post info status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)

    @property
    def has_microphone_icon(self):
        we = self._find_element_by_selector(selector=self._microphone_icon, timeout=0)
        return we.is_displayed() if we else False

    def _wait_active(self, timeout=0):
        self._we = self._find_myself()
        try:
            self._find_element_by_selector(selector=self._event_markets_list,
                                           bypass_exceptions=(NoSuchElementException,))
        except StaleElementReferenceException:
            self._we = self._find_myself()

    @property
    def race_details(self):
        return RaceDetailsContainer(selector=self._race_details_container, context=self._we)

    def has_post_info(self, timeout=2, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._post_info_container,
                                                   timeout=0) is not None,
            name=f'{self.__class__.__name__} – Post info status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)

    @property
    def post_info(self):
        return PostInfo(selector=self._post_info_container, context=self._we)

    @property
    def sorting_toggle(self):
        return SortingToggle(selector=self._sorting_toggle, context=self._we)

    @property
    def sorting_selector(self):
        return SortingToggleSelector(selector=self._sorting_selector, context=self._we, timeout=1)

    def has_sorting_toggle(self, timeout=2, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._sorting_toggle,
                                                   timeout=0) is not None,
            name=f'{self.__class__.__name__} – Sorting Toggle status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)

    @property
    def event_off_times_list(self):
        return self._event_off_times_list_type(selector=self._event_off_times_list, context=self._we)

    def has_event_off_times_list(self, timeout=2, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._event_off_times_list,
                                                   timeout=0) is not None,
            name=f'{self.__class__.__name__} – Event time off list status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)

    @property
    def active_off_time(self):
        return self.event_off_times_list.selected_item

    def has_video_stream_button(self, timeout=1, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._video_stream_button,
                                                   timeout=0) is not None,
            name=f'{self.__class__.__name__} – "Video Stream" button  status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)

    @property
    def video_stream_button(self):
        return ButtonBase(selector=self._video_stream_button, context=self._we)

    @property
    def event_markets_list(self):
        return self._event_markets_list_type(selector=self._event_markets_list, context=self._we)

    def has_watch_free_button(self, timeout=1, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._watch_free_button,
                                                   timeout=0) is not None,
            name=f'{self.__class__.__name__} – "Watch Free" button shown status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)

    @property
    def watch_free_button(self):
        return SpinnerButtonBase(selector=self._watch_free_button, context=self._we)

    @property
    def has_watch_free_area(self):
        we = self._find_element_by_selector(selector=self._watch_free_area, timeout=0)
        return we.is_displayed() if we else False

    @property
    def watch_free_area(self):
        return WatchFreeArea(selector=self._watch_free_area, context=self._we)

    @property
    def has_video_stream_area(self):
        we = self._find_element_by_selector(selector=self._video_stream_area, timeout=0)
        return 'ng-hide' not in we.get_attribute('class') if we else False

    @property
    def video_stream_area(self):
        return VideoStreamArea(selector=self._video_stream_area)

    def has_watch_free_info_link(self, timeout=1, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._watch_free_legend,
                                                   timeout=0) is not None,
            name=f'Event time off list status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)

    def has_live_commentary_link(self, timeout=1, expected_result=True):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._live_commentary_link, timeout=0),
                               name=f'"Live Commentary" link to be {expected_result}',
                               expected_result=expected_result,
                               timeout=timeout)

    @property
    def watch_free_info_link(self):
        return WatchFreeLink(selector=self._watch_free_legend)

    @property
    def stream_error(self):
        return self._get_webelement_text(selector=self._video_stream_error, timeout=3)

    def has_stream_error(self, expected_result=True, timeout=3, poll_interval=1):
        state = 'displayed' if expected_result else 'undisplayed'

        result = wait_for_result(lambda: self._find_element_by_selector(selector=self._video_stream_error, timeout=0),
                                 name=f'Stream error to be {state}',
                                 poll_interval=poll_interval,
                                 expected_result=expected_result,
                                 timeout=timeout)
        return result

    @property
    def specials_carousel(self):
        return self._specials_carousel_type(selector=self._specials_carousel, context=self._we)

    def has_specials_carousel(self, timeout=3, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._specials_carousel,
                                                   timeout=0) is not None,
            name=f'Special carousel status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)

    def choose_sorting_option(self, option):
        get_driver().implicitly_wait(2)
        self.sorting_toggle.open()
        self.sorting_selector.click_item(option)
        get_driver().implicitly_wait(0.7)


class RacingEventDetails(BaseContent):
    _url_pattern = r'^http[s]?:\/\/.+\/(horse-racing)\/[\w-]+\/[\w-]+\/[\w-]+\/[0-9]+(\/[\w-]+){0,1}'  # /market_part_url sometimes is not present
    _tab_content_type = RacingEDPTabContent
    _bet_finder_link = 'xpath=.//*[@data-crlat="betFinderLink"]'
    _bold_priced_section = 'xpath=.//*[@data-crlat="section.boldPriced"]'
    _sub_header = 'xpath=.//*[@data-crlat="topBar"]'
    _sub_header_type = SubHeader
    _meeting_selector = 'xpath=.//*[@data-crlat="meetingSelector"]'
    _breadcrumbs = 'xpath=.//*[@data-crlat="breadcrumbsContainer"]'
    _breadcrumbs_type = Breadcrumbs
    _event_title = 'xpath=.//*[@data-crlat="eventTitle"]'
    _meetings_list = 'xpath=.//*[@data-crlat="racingMeetingsContainer" or @class="desktop-list"]'
    _meetings_list_type = MeetingsList
    _item = 'xpath=.//*[@class="inner-container"]//div[@data-crlat="outcomeEntity"]'
    _list_item_type = RacingDetails
    _ew_terms = 'xpath=.//*[@data-crlat="terms" or @data-crlat="eachWayContainer"]'
    _show_info_link = 'xpath=.//*[contains(@class, "show-option")]'
    _tooltip_container = 'xpath=.//*[contains(@class, "tooltip-container")]'
    _my_stable_button = 'xpath=.//*[@data-crlat="myStableTitle"]'
    _my_stable_icon_link = 'xpath=.//*[@data-crlat="myStableIcon"]/*'
    _my_stable_icon = 'xpath=.//*[@data-crlat="myStableIcon"]'
    _edit_stable = 'xpath=.//*[@data-crlat="editSaveStable"]'

    _event_user_tabs = 'xpath=.//*[@data-crlat="userTabs" or contains(@class, "tabs-list")]'  # TODO data-crlat
    _event_user_tabs_list_type = EventUserTabsList

    _my_bets_section_list = 'tag=my-bets'
    _my_bets_sections_list_type = MyBetsTabContent

    @property
    def event_user_tabs_list(self):
        return self._event_user_tabs_list_type(self._event_user_tabs, context=self._we)

    @property
    def my_bets(self):
        return self._my_bets_sections_list_type(selector=self._my_bets_section_list, context=self._we)

    @property
    def my_stable_link(self):
        return ButtonBase(selector=self._my_stable_button)

    @property
    def my_stable_icon(self):
        return self._find_element_by_selector(selector=self._my_stable_icon)

    def has_my_stable_icon(self, expected_result=True, timeout=1):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._my_stable_icon, context=self._we,
                                                   timeout=0) is not None,
            name=f'"my stable" link presence status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)

    @property
    def my_stable_icon_link(self):
        return self._find_element_by_selector(selector=self._my_stable_icon_link).get_attribute('href')

    @property
    def edit_stable(self):
        return EditStable(selector=self._edit_stable)

    @property
    def has_tooltip_container(self):
        return self._find_element_by_selector(selector=self._tooltip_container, timeout=2) is not None

    _market_desc_text = 'xpath=.//*[@class="description-value"]'
    _market_desc_new_badge = 'xpath=.//*[@class="new-badge"]'
    _racing_post_verdict = 'xpath=.//*[@data-crlat="drawer.content"]'

    @property
    def racing_post_verdict(self):
        return RacePostVerdictOverlay(selector=self._racing_post_verdict)

    @property
    def show_info_link_text(self):
        return self._get_webelement_text(selector=self._show_info_link, context=self._we, timeout=2)

    @property
    def show_info_link(self):
        return ComponentBase(selector=self._show_info_link, timeout=2)

    @property
    def each_way_terms(self):
        return EachWayTerms(selector=self._ew_terms, context=self._we)

    @property
    def bet_filter_link(self):
        return ButtonBase(selector=self._bet_finder_link, context=self._we)

    @property
    def has_bet_filter_link(self):
        return self._find_element_by_selector(selector=self._bet_finder_link, timeout=2) is not None

    @property
    def sub_header(self):
        return self._sub_header_type(selector=self._sub_header, context=self._we)

    @property
    def meeting_selector(self):
        return ButtonBase(selector=self._meeting_selector, context=self._we)

    @property
    def breadcrumbs(self):
        return self._breadcrumbs_type(selector=self._breadcrumbs, context=self._we)

    @property
    def event_title(self):
        return self._get_webelement_text(selector=self._event_title, timeout=3)

    @property
    def meetings_list(self):
        return self._meetings_list_type(selector=self._meetings_list, context=self._we)

    @property
    def market_description_text(self):
        return ComponentBase(selector=self._market_desc_text, context=self._we, timeout=20)

    def has_market_desc_new_badge(self, timeout=5, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._market_desc_new_badge,
                                                   timeout=5) is not None,
            name=f'New Badge status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)

    def has_meeting_selector(self, timeout=1, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._meeting_selector,
                                                   timeout=0) is not None,
            name=f'Button status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)

    def has_market_description_text(self, timeout=5, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._market_desc_text,
                                                   timeout=5) is not None,
            name=f'Market Description status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)

    @property
    def market_description(self):
        return self._get_webelement_text(selector=self._market_desc_text, timeout=3)
