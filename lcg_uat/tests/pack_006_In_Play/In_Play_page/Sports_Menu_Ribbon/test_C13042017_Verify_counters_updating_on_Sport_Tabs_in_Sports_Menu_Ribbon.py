import pytest
from tests.base_test import vtest
from tests.Common import Common
from time import sleep
from voltron.utils.helpers import get_inplay_sports_ribbon
import voltron.environments.constants as vec


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  # Cannot create events on prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.in_play
@pytest.mark.desktop
@vtest
class Test_C13042017_Verify_counters_updating_on_Sport_Tabs_in_Sports_Menu_Ribbon(Common):
    """
    TR_ID: C13042017
    NAME: Verify counters updating on Sport Tabs in Sports Menu Ribbon
    DESCRIPTION: This test case verifies counters updating on Sport Tabs in Sports Menu Ribbon
    PRECONDITIONS: **CMS config:**
    PRECONDITIONS: 'InPlayWatchLive' should be enabled in CMS > System configuration > Structure > InPlayWatchLive
    PRECONDITIONS: **TI (events) config:**
    PRECONDITIONS: 1) Several sports should contain live events, upcoming events and events with 'Watch live' label
    PRECONDITIONS: CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: 1) Load the app
    PRECONDITIONS: 2) Navigate to 'In-Play' page from the Sports Menu Ribbon (for mobile/tablet) or 'Main Navigation' menu at the 'Universal Header' (for Desktop)
    PRECONDITIONS: 3) Select any sport
    PRECONDITIONS: **Note:**
    PRECONDITIONS: To check value that is displayed in Counter use the following instruction:
    PRECONDITIONS: Dev Tools->Network->WS
    PRECONDITIONS: Open 'INPLAY_SPORTS_RIBBON_CHANGED' response
    PRECONDITIONS: Look at **liveEventCount** attribute for live now events and **upcomingEventCount** attribute for upcoming events
    PRECONDITIONS: **Counters are NOT displayed for Ladbrokes mobile Inplay page. There is "Live" label next to Sport icon instead of counter.**
    """
    keep_browser_open = True
    live_now_switcher = vec.inplay.LIVE_NOW_SWITCHER
    upcoming_switcher = vec.inplay.UPCOMING_SWITCHER

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
        DESCRIPTION: 1) Several sports should contain live events, upcoming events and events with 'Watch live' label
        """
        self.__class__.start_time_upcoming = self.get_date_time_formatted_string(hours=10)
        self.upcoming_event_demo = self.ob_config.add_autotest_premier_league_football_event(is_upcoming=True,
                                                                                             perform_stream=True,
                                                                                             start_time=self.start_time_upcoming)
        self.__class__.upcoming_event_id_demo = self.upcoming_event_demo.event_id

        self.in_play_event_demo = self.ob_config.add_autotest_premier_league_football_event(is_live=True,
                                                                                            perform_stream=True)
        self.__class__.inplay_event_id_demo = self.in_play_event_demo.event_id
        self.upcoming_event = self.ob_config.add_autotest_premier_league_football_event(is_upcoming=True,
                                                                                        perform_stream=True,
                                                                                        start_time=self.start_time_upcoming)
        self.__class__.upcoming_event_id = self.upcoming_event.event_id

        self.in_play_event = self.ob_config.add_autotest_premier_league_football_event(is_live=True,
                                                                                       perform_stream=True)
        self.__class__.inplay_event_id = self.in_play_event.event_id
        self.in_play_event_2 = self.ob_config.add_autotest_premier_league_football_event(is_live=True,
                                                                                         perform_stream=True)
        self.__class__.inplay_event_id_2 = self.in_play_event_2.event_id
        self.ob_config.change_event_state(event_id=self.inplay_event_id_demo, displayed=True, active=True)
        self.ob_config.change_event_state(event_id=self.upcoming_event_id_demo, displayed=True, active=True)

    def test_001_in_ti_undisplayset_results_to_any_inplay_event_for_any_sportnoteattribute_displayedn_should_be_set_for_event_(self):
        """
        DESCRIPTION: In TI undisplay/set results to any inplay event for any sport
        DESCRIPTION: NOTE:
        DESCRIPTION: (attribute 'displayed="N"' should be set for event )
        EXPECTED: * Undisplayed/resulted event is removed from front-end automatically
        EXPECTED: Coral:
        EXPECTED: * Counter is updated for respective Sport in Sports Menu Ribbon
        EXPECTED: * Updated value in Counter corresponds to **liveEventCount** attribute in WS
        EXPECTED: Ladbrokes:
        EXPECTED: * Counter not displayed. "Live" label displayed instead of counter
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
        sleep(5)  # Takes time to reflect on UI
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

    def test_002_trigger_starting_of_inplay_event_for_any_sport(self):
        """
        DESCRIPTION: Trigger starting of inplay event for any sport
        EXPECTED: * Started event appears on front-end automatically
        EXPECTED: Coral:
        EXPECTED: * Counter is updated for respective Sport in Sports Menu Ribbon
        EXPECTED: * Updated value in Counter corresponds to **liveEventCount** attribute in WS
        EXPECTED: Ladbrokes:
        EXPECTED: * Counter not displayed. "Live" label displayed instead of counter
        """
        self.ob_config.change_event_state(event_id=self.inplay_event_id, displayed=True, active=True)
        sleep(5)  # Takes time to reflect on UI
        self.device.refresh_page()

    def test_003_step_for_desktopclick_on_upcoming_switcher(self):
        """
        DESCRIPTION: **Step for desktop:**
        DESCRIPTION: Click on 'Upcoming' switcher
        EXPECTED:
        """
        if self.device_type == 'desktop':
            self.site.inplay.tab_content.grouping_buttons.click_button(vec.inplay.UPCOMING_SWITCHER)
            upcoming_sports = self.site.inplay.inplay_sport_menu.items_as_ordered_dict
            self.assertTrue(upcoming_sports, msg='No Sports found in Upcoming tab')
        self.ob_config.change_event_state(event_id=self.upcoming_event_id, displayed=True, active=True)
        self.device.refresh_page()

    def test_004_in_ti_undisplayset_results_to_any_upcoming_event_for_any_sportnoteattribute_displayedn_should_be_set_for_event_(self):
        """
        DESCRIPTION: In TI undisplay/set results to any upcoming event for any sport
        DESCRIPTION: NOTE:
        DESCRIPTION: (attribute 'displayed="N"' should be set for event )
        EXPECTED: **For mobile/tablet:**
        EXPECTED: * Undisplayed/resulted event is removed from front-end automatically
        EXPECTED: Coral:
        EXPECTED: * Counter remains unchanged for respective Sport in Sports Menu Ribbon
        EXPECTED: Ladbrokes:
        EXPECTED: * Counter not displayed. "Live" label displayed instead of counter
        EXPECTED: **For desktop:**
        EXPECTED: * Undisplayed/resulted event is removed from front-end automatically
        EXPECTED: * Counter is updated for respective Sport in Sports Menu Ribbon
        EXPECTED: * Updated value in Counter corresponds to **upcomingEventCount** attribute in WS
        """
        parameters = get_inplay_sports_ribbon()
        upcoming_counter_before = parameters[0]['upcommingLiveStreamEventCount']
        self.ob_config.change_event_state(event_id=self.upcoming_event_id, displayed=False, active=False)
        sleep(5)  # Takes time to reflect on UI
        self.device.refresh_page()
        upcoming_counter_after = self.get_counter(self.upcoming_switcher)
        if self.device_type == 'desktop':
                self.assertNotEqual(upcoming_counter_before, upcoming_counter_after,
                                    msg=f'Value in Counter "{upcoming_counter_after}" does not corresponds to '
                                    f'"{upcoming_counter_before}" **liveStreamEventCount** attribute in WS')

    def test_005_trigger_appearing_of_upcoming_event_for_any_sport(self):
        """
        DESCRIPTION: Trigger appearing of upcoming event for any sport
        EXPECTED: **For mobile/tablet:**
        EXPECTED: * Event appears on front-end automatically
        EXPECTED: Coral:
        EXPECTED: * Counter remains unchanged for respective Sport in Sports Menu Ribbon
        EXPECTED: Ladbrokes:
        EXPECTED: * Counter not displayed. "Live" label displayed instead of counter
        EXPECTED: **For desktop:**
        EXPECTED: * Event appears on front-end automatically
        EXPECTED: * Counter is updated for respective Sport in Sports Menu Ribbon
        EXPECTED: * Updated value in Counter corresponds to **upcomingEventCount** attribute in WS
        """
        if self.device_type == 'mobile':
            upcoming_counter_before2 = self.get_counter(self.upcoming_switcher)
            self.__class__.start_time_upcoming = self.get_date_time_formatted_string(hours=5)
            self.upcoming_event_2 = self.ob_config.add_autotest_premier_league_football_event(is_upcoming=True,
                                                                                              perform_stream=True,
                                                                                              start_time=self.start_time_upcoming)
            self.upcoming_event_id_2 = self.upcoming_event_2.event_id
            self.ob_config.change_event_state(event_id=self.upcoming_event_id_2, displayed=True, active=True)
            sleep(6)  # Takes time to reflect on UI
            self.device.refresh_page()
            upcoming_counter_after2 = self.get_counter(self.upcoming_switcher)
            self.assertNotEqual(upcoming_counter_before2, upcoming_counter_after2,
                                msg=f'Value in Counter "{upcoming_counter_after2}" does not corresponds to '
                                f'"{upcoming_counter_before2}" **liveStreamEventCount** attribute in WS')
