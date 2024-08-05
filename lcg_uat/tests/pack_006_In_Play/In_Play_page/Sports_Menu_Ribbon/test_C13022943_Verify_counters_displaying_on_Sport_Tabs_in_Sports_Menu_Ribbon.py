import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.helpers import get_inplay_sports_ribbon


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod - unable create events with upcoming events
@pytest.mark.medium
@pytest.mark.in_play
@pytest.mark.desktop
@vtest
class Test_C13022943_Verify_counters_displaying_on_Sport_Tabs_in_Sports_Menu_Ribbon(Common):
    """
    TR_ID: C13022943
    NAME: Verify counters displaying on Sport Tabs in Sports Menu Ribbon
    DESCRIPTION: This test case verifies counters displaying on Sport Tabs in Sports Menu Ribbon
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
    PRECONDITIONS: "
    PRECONDITIONS: **Counters are NOT displayed for Ladbrokes mobile Inplay page. There is "Live" label next to Sport icon instead of counter.**
    """
    keep_browser_open = True

    def get_counter(self, sport):
        """
        :param section_name: section/switcher name
        :return: counter: counter with total number of in-play events for specific sport
        """
        counter = self.site.inplay.inplay_sport_menu.items_as_ordered_dict[sport].counter
        return counter

    def sport_counter_verification(self, sport):
        sport_tab = sport.upper() if self.brand == 'bma' else sport
        self.site.inplay.inplay_sport_menu.click_item(sport_tab)
        parameters = get_inplay_sports_ribbon()
        for param in parameters:
            try:
                catergory_name = param['categoryName']
            except Exception:
                continue
            if catergory_name == sport:
                ws_counter = param['liveEventCount']
                counter = self.get_counter(sport_tab)
                if self.brand == 'ladbrokes' and self.device_type == 'mobile':
                    self.softAssert(self.assertEqual, counter, 0,
                                    msg=f'Value in Counter "{counter}" does not corresponds to "LIVE" '
                                        f'**liveStreamEventCount** attribute in WS for sport "{sport}"')
                else:
                    self.softAssert(self.assertEqual, counter, ws_counter,
                                    msg=f'Value in Counter "{counter}" does not corresponds to "{ws_counter}" '
                                    f'**liveStreamEventCount** attribute in WS for sport "{sport}"')
                status = True
        self.assertTrue(status, msg=f'"{status}" sport counter is not verified for sport "{sport}"')

    def test_000_preconditions(self):
        """
        DESCRIPTION: 1) Several sports should contain live events, upcoming events and events with 'Watch live' label
        """
        start_time_upcoming = self.get_date_time_formatted_string(hours=10)
        self.ob_config.add_autotest_premier_league_football_event()
        self.ob_config.add_autotest_cricket_event(is_upcoming=True, perform_stream=True,
                                                  start_time=start_time_upcoming)
        self.ob_config.add_autotest_cricket_event(is_live=True, perform_stream=True,)
        self.ob_config.add_hockey_event_to_super_league(is_live=True)
        self.ob_config.add_tennis_event_to_autotest_trophy(is_upcoming=True, perform_stream=True,
                                                           start_time=start_time_upcoming)

    def test_001_for_mobiletabletverify_counter_displaying_next_to_watch_live_icon(self):
        """
        DESCRIPTION: **For mobile/tablet:**
        DESCRIPTION: Verify Counter displaying next to 'Watch Live' icon
        EXPECTED: Counter is NOT displayed next to 'Watch Live' icon
        """
        self.navigate_to_page(name='/in-play')
        self.device.refresh_page()
        self.site.wait_content_state(state_name=vec.sb.TABS_NAME_IN_PLAY)
        self.site.inplay.inplay_sport_menu.click_item(vec.sb.WATCH_LIVE_LABEL)
        watch_live_counter = self.site.inplay.inplay_sport_menu.items_as_ordered_dict[vec.sb.WATCH_LIVE_LABEL].counter
        self.softAssert(self.assertEqual, 0, watch_live_counter, msg='The counter exists for watch live tab ')
        if self.device_type == 'desktop':
            self.site.inplay.tab_content.grouping_buttons.click_button(vec.inplay.UPCOMING_SWITCHER)
            watch_live_counter = self.site.inplay.inplay_sport_menu.items_as_ordered_dict[
                vec.sb.WATCH_LIVE_LABEL].counter
            self.softAssert(self.assertEqual, 0, watch_live_counter, msg='The counter exists for watch live tab ')

    def test_002_for_mobiletablet_select_sport_that_has_both_inplay_and_upcoming_events_verify_counter(self):
        """
        DESCRIPTION: **For mobile/tablet:**
        DESCRIPTION: * Select sport that has both inplay and upcoming events
        DESCRIPTION: * Verify Counter
        EXPECTED: Coral:
        EXPECTED: * Value in Counter corresponds to **liveEventCount** attribute for selected sport
        EXPECTED: * Count of upcoming events is ignored
        EXPECTED: Ladbrokes:
        EXPECTED: * Counter not displayed. "Live" label displayed instead of counter ![](index.php?/attachments/get/36085)
        """
        self.sport_counter_verification(sport=vec.bma.CRICKET)

    def test_003_for_mobiletablet_select_sport_that_has_only_inplay_events_verify_counter(self):
        """
        DESCRIPTION: **For mobile/tablet:**
        DESCRIPTION: * Select sport that has ONLY inplay events
        DESCRIPTION: * Verify Counter
        EXPECTED: Coral:
        EXPECTED: * Value in Counter corresponds to **liveEventCount** attribute for selected sport
        EXPECTED: Ladbrokes:
        EXPECTED: * Counter not displayed. "Live" label displayed instead of counter
        """
        self.sport_counter_verification(sport=vec.olympics.HOCKEY)

    def test_004_for_mobiletablet_select_sport_that_has_only_upcoming_events_verify_counter(self):
        """
        DESCRIPTION: **For mobile/tablet:**
        DESCRIPTION: * Select sport that has ONLY upcoming events
        DESCRIPTION: * Verify Counter
        EXPECTED: Coral:
        EXPECTED: * Counter is not shown
        EXPECTED: ![](index.php?/attachments/get/30603)
        EXPECTED: Ladbrokes: Counter and Live label not shown
        EXPECTED: ![](index.php?/attachments/get/36086)
        """
        self.sport_counter_verification(sport=vec.olympics.TENNIS)

    def test_005_for_desktop_select_watch_live_tab__live_now_switcher_verify_counter_next_to__watch_live_icon(self):
        """
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: * Select 'Watch Live' tab > 'Live now' switcher
        DESCRIPTION: * Verify Counter next to  'Watch Live' icon
        EXPECTED: Counter is NOT displayed next to 'Watch Live' icon
        """
        # covered in step 1

    def test_006_for_desktop_select_watch_live_tab__upcoming_switcher_verify_counter_next_to__watch_live_icon(self):
        """
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: * Select 'Watch Live' tab > 'Upcoming' switcher
        DESCRIPTION: * Verify Counter next to  'Watch Live' icon
        EXPECTED: Counter is NOT displayed next to 'Watch Live' icon
        """
        # covered in step 1

    def test_007_for_desktop_select_any_sport__live_now_switcher_verify_counter_next_to_sport_icon(self):
        """
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: * Select any sport > 'Live now' switcher
        DESCRIPTION: * Verify Counter next to sport icon
        EXPECTED: * Value in Counter corresponds to **liveEventCount** attribute for selected sport
        EXPECTED: * Counter is not shown if sport contains no live events
        """
        # covered in step 2,3,4

    def test_008_for_desktop_select_any_sport__upcoming_switcher_verify_counter_next_to_sport_icon(self):
        """
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: * Select any sport > 'Upcoming' switcher
        DESCRIPTION: * Verify Counter next to sport icon
        EXPECTED: * Value in Counter corresponds to **upcomingEventCount** attribute for selected sport
        EXPECTED: * Counter is not shown if sport contains no upcoming events
        """
        if self.device_type == 'desktop':
            sport = vec.bma.CRICKET.upper() if self.brand == 'bma' else vec.bma.CRICKET
            self.site.inplay.inplay_sport_menu.click_item(sport)
            switcher_tab = self.site.inplay.tab_content.grouping_buttons.items_as_ordered_dict[vec.inplay.UPCOMING_SWITCHER]
            parameters = get_inplay_sports_ribbon()
            for param in parameters:
                try:
                    catergory_name = param['categoryName']
                except Exception:
                    continue
                if catergory_name == 'Cricket':
                    ws_counter = param['upcomingEventCount']
                    counter = switcher_tab.counter
                    self.softAssert(self.assertEqual, counter, ws_counter,
                                    msg=f'Value in Counter "{counter}" does not corresponds to "{ws_counter}" '
                                    f'**liveStreamEventCount** attribute in WS')
                    status = True
            self.assertTrue(status, msg='Sport not verified')
