import pytest
import voltron.environments.constants as vec
from time import sleep
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.helpers import get_inplay_sports_ribbon


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # Can not create events in prod
@pytest.mark.medium
@pytest.mark.in_play
@pytest.mark.desktop
@vtest
class Test_C333898_Verify_Live_now_and_Upcoming_counters_updating(BaseSportTest):
    """
    TR_ID: C333898
    NAME: Verify 'Live now' and 'Upcoming' counters updating
    DESCRIPTION: This test case verifies Counters updating next to 'Live now' and 'Upcoming' sections/switchers on in-play pages
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
    PRECONDITIONS: Open 'INPLAY_LS_SPORTS_RIBBON' response
    PRECONDITIONS: Look at **liveEventCount** attribute for live now events and **upcomingEventCount** attribute for upcoming events
    PRECONDITIONS: **NOTE:**
    PRECONDITIONS: We receive counters value in Sport ribbon , in "All sports" category.
    PRECONDITIONS: For Counters to update correctly on Watch Live tab the following configuration should **ALWAYS** be made/verified:
    PRECONDITIONS: CMS Sport category **"All sports"**
    PRECONDITIONS: should have Id = 0
    PRECONDITIONS: Should have Target Uri = allsports
    PRECONDITIONS: Should have SS Category Code = ALL_SPORTS
    PRECONDITIONS: Should be active and checkbox "Show In Play" should be active
    """
    keep_browser_open = True
    live_now_switcher = vec.inplay.LIVE_NOW_SWITCHER
    upcoming_switcher = vec.inplay.UPCOMING_SWITCHER
    markets = [('to_qualify',)]

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
        DESCRIPTION: Create test event and log in
        """
        self.__class__.expected_market = 'AUTO TEST - AUTOTEST PREMIER LEAGUE' if self.device_type == 'desktop' \
            else 'AUTOTEST PREMIER LEAGUE'
        self.__class__.sport_name = 'Football' if self.brand == 'bma' else 'FOOTBALL'
        start_time_upcoming = self.get_date_time_formatted_string(hours=10)
        self.__class__.in_play_event = self.ob_config.add_autotest_premier_league_football_event(is_live=True,
                                                                                                 perform_stream=True,
                                                                                                 markets=self.markets)
        self.__class__.inplay_event_id = self.in_play_event.event_id
        self.__class__.inplay_team_1 = self.in_play_event.team1
        self.__class__.inplay_team_2 = self.in_play_event.team2
        self.__class__.upcoming_event = self.ob_config.add_autotest_premier_league_football_event(is_upcoming=True,
                                                                                                  perform_stream=True,
                                                                                                  start_time=start_time_upcoming,
                                                                                                  markets=self.markets)
        self.__class__.upcoming_event_id = self.upcoming_event.event_id
        self.__class__.upcoming_team_1 = self.upcoming_event.team1
        self.__class__.upcoming_team_2 = self.upcoming_event.team1

    def test_001_in_ti_undisplayset_results_to_any_events_from_watch_live_tab__live_now_and_upcoming_events_sectionswitchernoteattribute_displayedn_should_be_set_for_event_(self):
        """
        DESCRIPTION: In TI undisplay/set results to any events from 'Watch live' tab > 'Live now' and 'Upcoming events' section/switcher
        DESCRIPTION: NOTE:
        DESCRIPTION: (attribute 'displayed="N"' should be set for event )
        EXPECTED: * Undisplayed/resulted event is removed from front-end automatically
        EXPECTED: * Counter next 'Live now' and 'Upcoming events' section/switcher is updated
        EXPECTED: * Updated value in Counter corresponds to **liveStreamEventCount** and ** upcomingLiveStreamEventCount**attribute in WS ('All sports' item)
        """
        self.navigate_to_page('/in-play/football')
        live_counter_before = self.get_counter(self.live_now_switcher)
        upcoming_counter_before = self.get_counter(self.upcoming_switcher)
        if self.device_type == 'mobile':
            page_headers = list(self.site.inplay.tab_content.items_as_ordered_dict.keys())
            self.assertIn(vec.inplay.LIVE_NOW_EVENTS_SECTION, page_headers,
                          msg=f'No "{vec.inplay.LIVE_NOW_EVENTS_SECTION}" section is found on In-Play page')
            self.assertIn(vec.inplay.UPCOMING_EVENTS_SECTION, page_headers,
                          msg=f'No "{vec.inplay.UPCOMING_EVENTS_SECTION}" section is found on In-Play page')

        self.ob_config.change_event_state(event_id=self.inplay_event_id, displayed=False, active=False)
        self.ob_config.change_event_state(event_id=self.upcoming_event_id, displayed=False, active=False)
        sleep(5)
        self.device.refresh_page()
        if live_counter_before != 0:
            live_counter_after = self.get_counter(self.live_now_switcher)
            self.assertNotEqual(live_counter_before, live_counter_after,
                                msg=f'Value in Counter "{live_counter_after}" does not corresponds to '
                                    f'"{live_counter_before}" **liveStreamEventCount** attribute in WS')

        if upcoming_counter_before != 0:
            upcoming_counter_after = self.get_counter(self.upcoming_switcher)
            self.assertNotEqual(upcoming_counter_before, upcoming_counter_after,
                                msg=f'Value in Counter "{upcoming_counter_before}" does not corresponds to '
                                    f'"{upcoming_counter_after}" **upcomingLiveStreamEventCount** attribute in WS')

    def test_002_trigger_starting_of_inplay_and_upcoming_events_with_streaming_mapped(self):
        """
        DESCRIPTION: Trigger starting of inplay and upcoming events with streaming mapped
        EXPECTED: * Started events appear on front-end automatically
        EXPECTED: * Counter next 'Live now' and 'Upcoming events' section/switcher is updated
        EXPECTED: * Updated value in Counter corresponds to **liveStreamEventCount** and ** upcomingLiveStreamEventCount**attribute in WS ('All sports' item)
        """
        parameters = get_inplay_sports_ribbon()
        counter = self.get_counter(self.upcoming_switcher)
        self.ob_config.change_event_state(event_id=self.inplay_event_id, displayed=True, active=True)
        self.ob_config.change_event_state(event_id=self.upcoming_event_id, displayed=True, active=True)

        ws_counter = parameters[0]['upcommingLiveStreamEventCount']
        self.softAssert(self.assertNotEqual, counter, ws_counter,
                        msg=f'Value in Counter "{counter}" does not corresponds to "{ws_counter}" '
                            f'**upcomingLiveStreamEventCount** attribute in WS')
        ws_counter = parameters[0]['liveStreamEventCount']
        counter = self.get_counter(self.live_now_switcher)
        self.softAssert(self.assertNotEqual, counter, ws_counter,
                        msg=f'Value in Counter "{counter}" does not corresponds to "{ws_counter}" '
                            f'**liveStreamEventCount** attribute in WS')

    def test_003__select_any_sport_in_sports_menu_ribbon_in_ti_undisplayset_results_to_any_inplay_and_upcoming_events_from_selected_sportnoteattribute_displayedn_should_be_set_for_event_(self):
        """
        DESCRIPTION: * Select any sport in Sports Menu Ribbon
        DESCRIPTION: * In TI undisplay/set results to any inplay and upcoming events from selected sport
        DESCRIPTION: NOTE:
        DESCRIPTION: (attribute 'displayed="N"' should be set for event )
        EXPECTED: * Undisplayed/resulted event is removed from front-end automatically
        EXPECTED: * Counter next 'Live now' and 'Upcoming events' section/switcher is updated
        EXPECTED: * Updated value in Counter corresponds to **liveEventCount** and ** upcomingEventCount**attribute in WS (respective sport item)
        """
        # Covered in step 1

    def test_004_trigger_starting_of_inplay_and_upcoming_events_for_the_same_sport(self):
        """
        DESCRIPTION: Trigger starting of inplay and upcoming events for the same sport
        EXPECTED: * Started events appear on front-end automatically
        EXPECTED: * Counter next 'Live now' and 'Upcoming events' section/switcher is updated
        EXPECTED: * Updated value in Counter corresponds to **liveEventCount** and ** upcomingEventCount**attribute in WS (respective sport item)
        """
        # Covered in step 2

    def test_005__navigate_to_sport_landing_page__in_play_tab_in_ti_undisplayset_results_to_any_inplay_and_upcoming_events_from_selected_sportnoteattribute_displayedn_should_be_set_for_event_(self):
        """
        DESCRIPTION: * Navigate to Sport Landing page > 'In-play' tab
        DESCRIPTION: * In TI undisplay/set results to any inplay and upcoming events from selected sport
        DESCRIPTION: NOTE:
        DESCRIPTION: (attribute 'displayed="N"' should be set for event )
        EXPECTED: * Undisplayed/resulted event is removed from front-end automatically
        EXPECTED: * Counter next 'Live now' and 'Upcoming events' section/switcher is updated
        EXPECTED: * Updated value in Counter corresponds to **liveEventCount** and ** upcomingEventCount**attribute in WS (respective sport item)
        """
        self.navigate_to_page(name='sport/football')
        self.site.wait_content_state('football')
        in_play_tab = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.in_play,
                                              self.ob_config.football_config.category_id)
        self.site.football.tabs_menu.click_button(button_name=in_play_tab)
        live_counter_before = self.get_counter(self.live_now_switcher)

        self.ob_config.change_event_state(event_id=self.inplay_event_id, displayed=False, active=False)
        self.ob_config.change_event_state(event_id=self.upcoming_event_id, displayed=False, active=False)
        sleep(5)
        self.device.refresh_page()
        live_counter_after = self.get_counter(self.live_now_switcher)
        self.assertNotEqual(live_counter_before, live_counter_after,
                            msg=f'Value in Counter "{live_counter_before}" does not corresponds to '
                                f'"{live_counter_after}" **liveStreamEventCount** attribute in WS')

    def test_006_trigger_starting_of_inplay_and_upcoming_events_for_the_same_sport(self):
        """
        DESCRIPTION: Trigger starting of inplay and upcoming events for the same sport
        EXPECTED: * Started events appear on front-end automatically
        EXPECTED: * Counter next 'Live now' and 'Upcoming events' section/switcher is updated
        EXPECTED: * Updated value in Counter corresponds to **liveEventCount** and ** upcomingEventCount**attribute in WS (respective sport item)
        """
        live_counter_before = self.get_counter(self.live_now_switcher)

        self.ob_config.change_event_state(event_id=self.inplay_event_id, displayed=True, active=True)
        self.ob_config.change_event_state(event_id=self.upcoming_event_id, displayed=True, active=True)
        sleep(5)
        self.device.refresh_page()
        live_counter_after = self.get_counter(self.live_now_switcher)
        self.assertNotEqual(live_counter_before, live_counter_after,
                            msg=f'Value in Counter "{live_counter_before}" does not corresponds to '
                                f'"{live_counter_after}" **liveStreamEventCount** attribute in WS')

    def test_007_for_mobiletablet_navigate_to_home_page__in_play_tab_in_ti_undisplayset_results_to_any_inplay_and_upcoming_events(self):
        """
        DESCRIPTION: **For mobile/tablet:**
        DESCRIPTION: * Navigate to Home page > 'In-play' tab
        DESCRIPTION: * In TI undisplay/set results to any inplay and upcoming events
        EXPECTED: * Undisplayed/resulted event is removed from front-end automatically
        EXPECTED: * Counter next 'Live now See All' and 'Upcoming events' sections is updated
        EXPECTED: * Updated value in Counter corresponds to **liveEventCount** and ** upcomingEventCount**attribute in WS ('All sports' item)
        """
        if self.brand == 'mobile':
            self.navigate_to_page(name='home/in-play')
            self.site.wait_content_state(state_name='Homepage')
            live_counter_before = self.get_counter(self.live_now_switcher)

            self.ob_config.change_event_state(event_id=self.inplay_event_id, displayed=False, active=False)
            self.ob_config.change_event_state(event_id=self.upcoming_event_id, displayed=False, active=False)
            self.device.refresh_page()
            sleep(5)
            live_counter_after = self.get_counter(self.live_now_switcher)
            self.softAssert(self.assertNotEqual, live_counter_before, live_counter_after,
                            msg=f'Value in Counter "{live_counter_after}" does not corresponds to '
                                f'"{live_counter_after}"**liveStreamEventCount** attribute in WS')

    def test_008_for_mobiletablettrigger_starting_of_any_inplay_and_upcoming_events(self):
        """
        DESCRIPTION: **For mobile/tablet:**
        DESCRIPTION: Trigger starting of any inplay and upcoming events
        EXPECTED: * Started events appear on front-end automatically
        EXPECTED: * Counter next 'Live now See All' and 'Upcoming events' sections is updated
        EXPECTED: * Updated value in Counter corresponds to **liveEventCount** and ** upcomingEventCount**attribute in WS ('All sports' item)
        """
        if self.brand == 'mobile':
            live_counter_before = self.get_counter(self.live_now_switcher)

            self.ob_config.change_event_state(event_id=self.inplay_event_id, displayed=True, active=True)
            self.ob_config.change_event_state(event_id=self.upcoming_event_id, displayed=True, active=True)
            self.device.refresh_page()
            sleep(5)
            live_counter_after = self.get_counter(self.live_now_switcher)
            self.softAssert(self.assertNotEqual, live_counter_before, live_counter_after,
                            msg=f'Value in Counter "{live_counter_after}" does not corresponds to '
                                f'"{live_counter_before}" **liveStreamEventCount** attribute in WS')
