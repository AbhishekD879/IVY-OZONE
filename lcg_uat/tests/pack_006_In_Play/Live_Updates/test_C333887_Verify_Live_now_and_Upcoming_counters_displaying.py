import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.helpers import get_inplay_sports_ribbon


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.in_play
@pytest.mark.desktop
@vtest
class Test_C333887_Verify_Live_now_and_Upcoming_counters_displaying(BaseSportTest):
    """
    TR_ID: C333887
    NAME: Verify 'Live now' and 'Upcoming' counters displaying
    DESCRIPTION: This test case verifies Counters displaying next to 'Live now' and 'Upcoming' sections/switchers on in-play pages
    PRECONDITIONS: **CMS config:**
    PRECONDITIONS: 'InPlayWatchLive' should be enabled in CMS > System configuration > Structure > InPlayWatchLive
    PRECONDITIONS: **TI (events) config:**
    PRECONDITIONS: 1) Several sports should contain live events, upcoming events and events with 'Watch live' label
    PRECONDITIONS: CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: 1) Load the app
    PRECONDITIONS: 2) Navigate to 'In-Play' page from the Sports Menu Ribbon (for mobile/tablet) or 'Main Navigation' menu at the 'Universal Header' (for Desktop)
    PRECONDITIONS: 3) Click on 'Watch live' tab
    PRECONDITIONS: **Note:**
    PRECONDITIONS: To check value that is displayed in Counter use the following instruction:
    PRECONDITIONS: Dev Tools->Network->WS
    PRECONDITIONS: Open 'INPLAY_SPORTS_RIBBON' response
    PRECONDITIONS: Look at **liveEventCount** attribute for live now events and **upcomingEventCount** attribute for upcoming events
    """
    keep_browser_open = True
    upcoming = None
    sport_name = vec.sb.TABS_NAME_IN_PLAY
    live_now_switcher = vec.inplay.LIVE_NOW_SWITCHER
    upcoming_switcher = vec.inplay.UPCOMING_SWITCHER

    @classmethod
    def custom_setUp(cls):
        inplay_watch_live_section = cls.get_initial_data_system_configuration().get('InPlayWatchLive', {})
        if not inplay_watch_live_section:
            inplay_watch_live_section = cls.get_cms_config().get_system_configuration_item('InPlayWatchLive')
        if not inplay_watch_live_section.get('enabled'):
            raise CmsClientException('"InPlayWatchLive" is disabled in CMS')

    def get_counter(self, section_name):
        """
        :param section_name: section/switcher name
        :return: counter: counter with total number of in-play events for specific sport
        """
        if self.device_type != 'desktop':
            if section_name == self.live_now_switcher:
                has_counter = self.site.inplay.tab_content.has_live_now_counter()
                counter = self.site.inplay.tab_content.live_now_counter
            else:
                has_counter = self.site.inplay.tab_content.has_upcoming_counter()
                counter = self.site.inplay.tab_content.upcoming_counter
        else:
            switcher_tab = self.site.inplay.tab_content.grouping_buttons.items_as_ordered_dict[section_name]
            has_counter = switcher_tab.has_counter()
            counter = switcher_tab.counter
        if counter != 0:
            self.assertTrue(has_counter, msg='Counter with total number of in-play events is not displayed')
        return counter

    def test_000_preconditions(self):
        """
        DESCRIPTION: Add initial events: American Football, Tennis, Basketball
        EXPECTED: Initial events: American Football, Tennis, Basketball added
        """
        if self.brand == 'ladbrokes' and self.device_type == 'desktop':
            self.__class__.live_now_switcher = self.live_now_switcher.upper()
            self.__class__.upcoming_switcher = self.upcoming_switcher.upper()
        self.ob_config.add_american_football_event_to_autotest_league(is_live=True)
        self.ob_config.add_tennis_event_to_autotest_trophy(is_live=True)
        self.ob_config.add_basketball_event_to_autotest_league(is_live=True)
        upcoming = self.get_date_time_formatted_string(hours=2)
        self.ob_config.add_tennis_event_to_autotest_trophy(start_time=upcoming, is_upcoming=True)
        self.ob_config.add_basketball_event_to_autotest_league(start_time=upcoming, is_upcoming=True)
        self.navigate_to_page(name='/in-play')
        self.site.wait_content_state(state_name=self.sport_name)
        self.site.inplay.inplay_sport_menu.click_item(vec.sb.WATCH_LIVE_LABEL)

    def test_001_verify_counter_next_to_live_now_section_switcher(self):
        """
        DESCRIPTION: Verify counter next to 'Live now' section/switcher
        EXPECTED: * Counter with total number of in-play events with streaming mapped is displayed next to 'Live Now' inscription
        EXPECTED: * Value in Counter corresponds to **liveStreamEventCount** attribute in WS ('All sports' item)
        """
        parameters = get_inplay_sports_ribbon()
        ws_counter = parameters[0]['liveStreamEventCount']
        counter = self.get_counter(self.live_now_switcher)
        self.softAssert(self.assertEqual, counter, ws_counter,
                        msg=f'Value in Counter "{counter}" does not corresponds to "{ws_counter}" '
                            f'**liveStreamEventCount** attribute in WS')

    def test_002_for_mobile_tablet_scroll_down_till_upcoming_events_section_and_verify_counter_for_desktop_select_upcoming_switcher_and_verify_counter(self):
        """
        DESCRIPTION: **For mobile/tablet:**
        DESCRIPTION: Scroll down till 'Upcoming events' section and verify counter
        DESCRIPTION: **For desktop:**
        DESCRIPTION: Select 'Upcoming' switcher and verify counter
        EXPECTED: * Counter with total number of upcoming events with streaming mapped is displayed next to 'Upcoming events' or 'Upcoming' inscription
        EXPECTED: * Value in Counter corresponds to **upcomingLiveStreamEventCount** attribute in WS ('All sports' item)
        """
        counter = self.get_counter(self.upcoming_switcher)
        parameters = get_inplay_sports_ribbon()
        ws_counter = parameters[0]['upcommingLiveStreamEventCount']
        self.softAssert(self.assertEqual, counter, ws_counter,
                        msg=f'Value in Counter "{counter}" does not corresponds to "{ws_counter}" '
                            f'**upcomingLiveStreamEventCount** attribute in WS')

    def test_003_select_any_sport_in_sports_menu_ribbon_verify_counter_next_to_live_now_sections_switcher(self):
        """
        DESCRIPTION: * Select any sport in Sports Menu Ribbon
        DESCRIPTION: * Verify counter next to 'Live now' section/switcher
        EXPECTED: * Counter with total number of in-play events for specific sport is displayed next to 'Live Now' inscription
        EXPECTED: * Value in Counter corresponds to **liveEventCount** attribute in WS (respective sport item)
        """
        sport_title = vec.siteserve.TENNIS_TAB if not self.brand == 'ladbrokes' else vec.siteserve.TENNIS_TAB.title()
        self.site.inplay.inplay_sport_menu.click_item(sport_title)
        parameters = get_inplay_sports_ribbon()
        for item in parameters:
            if item['ssCategoryCode'].lower() == sport_title.lower():
                self.__class__.ws_counter = item['liveEventCount']
                break
        counter = self.get_counter(self.live_now_switcher)
        self.softAssert(self.assertEqual, counter, self.ws_counter,
                        msg=f'Value in Counter "{counter}" does not corresponds to "{self.ws_counter}" '
                        f'**liveEventCount** attribute in WS')

    def test_004_for_mobile_tablet_scroll_down_till_upcoming_events_section_and_verify_counter_for_desktop_select_upcoming_switcher_and_verify_counter(self):
        """
        DESCRIPTION: **For mobile/tablet:**
        DESCRIPTION: Scroll down till 'Upcoming events' section and verify counter
        DESCRIPTION: **For desktop:**
        DESCRIPTION: Select 'Upcoming' switcher and verify counter
        EXPECTED: * Counter with total number of upcoming events for specific sport is displayed next to 'Upcoming events' or 'Upcoming' inscription
        EXPECTED: * Value in Counter corresponds to **upcomingEventCount** attribute in WS (respective sport item)
        """
        counter = self.get_counter(self.upcoming_switcher)
        parameters = get_inplay_sports_ribbon()
        for item in parameters:
            if item['ssCategoryCode'].lower() == vec.siteserve.TENNIS_TAB.lower():
                self.__class__.ws_counter = item['upcomingEventCount']
                break
        self.softAssert(self.assertEqual, counter, self.ws_counter,
                        msg=f'Value in Counter "{counter}" does not corresponds to "{self.ws_counter}" '
                            f'**upcomingEventCount** attribute in WS')

    def test_005_navigate_to_sport_landing_page_in_play_tab_verify_counters_next_to_live_now_and_upcoming_events_upcoming_for_desktop(self):
        """
        DESCRIPTION: * Navigate to Sport Landing page > 'In-play' tab
        DESCRIPTION: * Verify counters next to 'Live now' and 'Upcoming events'/'Upcoming' for Desktop
        EXPECTED: * Value in 'Live now' counter corresponds to **liveEventCount** attribute in WS (respective sport item)
        EXPECTED: * Value in 'Upcoming events' counter corresponds to **upcomingEventCount** attribute in WS (respective sport item)
        """
        self.navigate_to_page(name='sport/basketball')
        self.site.wait_content_state(state_name='Basketball')
        in_play_tab = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.in_play,
                                              self.ob_config.basketball_config.category_id)
        result = self.site.basketball.tabs_menu.click_button(in_play_tab)
        self.assertTrue(result, msg=f'"{in_play_tab}" tab was not opened')
        live_counter = self.get_counter(self.live_now_switcher)
        parameters = get_inplay_sports_ribbon()
        for item in parameters:
            if item['ssCategoryCode'].lower() == vec.siteserve.BASKETBALL_TAB.lower():
                self.__class__.ws_counter = item['liveEventCount']
                break
        self.softAssert(self.assertEqual, live_counter, self.ws_counter,
                        msg=f'Value in Counter "{live_counter}" does not corresponds to "{self.ws_counter}" '
                        f'**liveEventCount** attribute in WS')
        upcoming_counter = self.get_counter(self.upcoming_switcher)
        parameters = get_inplay_sports_ribbon()
        for item in parameters:
            if item['ssCategoryCode'].lower() == vec.siteserve.BASKETBALL_TAB.lower():
                self.__class__.ws_counter = item['upcomingEventCount']
                break
        self.softAssert(self.assertEqual, upcoming_counter, self.ws_counter,
                        msg=f'Value in Counter "{upcoming_counter}" does not corresponds to "{self.ws_counter}" '
                        f'**upcomingEventCount** attribute in WS')

    def test_006_for_mobile_tablet_navigate_to_home_page_in_play_tab_verify_counters_next_to_live_now_see_all_and_upcoming_events(self):
        """
        DESCRIPTION: **For mobile/tablet:**
        DESCRIPTION: * Navigate to Home page > 'In-play' tab
        DESCRIPTION: * Verify counters next to 'Live now See All' and 'Upcoming events'
        EXPECTED: * Value in 'Live now See All' counter corresponds to **liveEventCount** attribute in WS ('All sports' item)
        EXPECTED: * Value in 'Upcoming events' counter corresponds to **upcomingEventCount** attribute in WS ('All sports' item)
        """
        if self.device_type != 'desktop':
            self.navigate_to_page(name='home/in-play')
            self.site.wait_content_state(state_name='Homepage')
            live_counter = self.site.home.tab_content.live_now.live_now_header.events_count_label
            parameters = get_inplay_sports_ribbon()
            ws_counter = parameters[0]['liveEventCount']
            self.softAssert(self.assertEqual, int(live_counter), ws_counter,
                            msg=f'Value in Counter "{live_counter}" does not corresponds to "{ws_counter}" '
                                f'**liveEventCount** attribute in WS')
            upcoming_counter = self.get_counter(self.upcoming_switcher)
            parameters = get_inplay_sports_ribbon()
            ws_counter = parameters[0]['upcomingEventCount']
            self.softAssert(self.assertEqual, upcoming_counter, ws_counter,
                            msg=f'Value in Counter "{upcoming_counter}" does not corresponds to "{ws_counter}"'
                                f' **upcomingEventCount** attribute in WS')
