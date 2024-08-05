import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.in_play
@vtest
class Test_C333887_Verify_Live_now_and_Upcoming_counters_displaying(Common):
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
    PRECONDITIONS: Dev Tools->Network->WS > inplay-publisher-tst0.coralsports.nonprod.cloud.ladbrokescoral.com/websocket/?EIO=3&transport=web
    PRECONDITIONS: Open 'INPLAY_SPORTS_RIBBON' response
    PRECONDITIONS: Look at **liveEventCount** attribute for live now events and **upcomingEventCount** attribute for upcoming events
    """
    keep_browser_open = True

    def test_001_verify_counter_next_to_live_now_sectionswitcher(self):
        """
        DESCRIPTION: Verify counter next to 'Live now' section/switcher
        EXPECTED: * Counter with total number of in-play events with streaming mapped is displayed next to 'Live Now' inscription
        EXPECTED: * Value in Counter corresponds to **liveStreamEventCount** attribute in WS ('All sports' item)
        """
        pass

    def test_002_for_mobiletabletscroll_down_till_upcoming_events_section_and_verify_counterfor_desktopselect_upcoming_switcher_and_verify_counter(self):
        """
        DESCRIPTION: **For mobile/tablet:**
        DESCRIPTION: Scroll down till 'Upcoming events' section and verify counter
        DESCRIPTION: **For desktop:**
        DESCRIPTION: Select 'Upcoming' switcher and verify counter
        EXPECTED: * Counter with total number of upcoming events with streaming mapped is displayed next to 'Upcoming events' or 'Upcoming' inscription
        EXPECTED: * Value in Counter corresponds to **upcomingLiveStreamEventCount** attribute in WS ('All sports' item)
        """
        pass

    def test_003__select_any_sport_in_sports_menu_ribbon_verify_counter_next_to_live_now_sectionswitcher(self):
        """
        DESCRIPTION: * Select any sport in Sports Menu Ribbon
        DESCRIPTION: * Verify counter next to 'Live now' section/switcher
        EXPECTED: * Counter with total number of in-play events for specific sport is displayed next to 'Live Now' inscription
        EXPECTED: * Value in Counter corresponds to **liveEventCount** attribute in WS (respective sport item)
        """
        pass

    def test_004_for_mobiletabletscroll_down_till_upcoming_events_section_and_verify_counterfor_desktopselect_upcoming_switcher_and_verify_counter(self):
        """
        DESCRIPTION: **For mobile/tablet:**
        DESCRIPTION: Scroll down till 'Upcoming events' section and verify counter
        DESCRIPTION: **For desktop:**
        DESCRIPTION: Select 'Upcoming' switcher and verify counter
        EXPECTED: * Counter with total number of upcoming events for specific sport is displayed next to 'Upcoming events' or 'Upcoming' inscription
        EXPECTED: * Value in Counter corresponds to **upcomingEventCount** attribute in WS (respective sport item)
        """
        pass

    def test_005__navigate_to_sport_landing_page__in_play_tab_verify_counters_next_to_live_now_and_upcoming_eventsupcoming_for_desktop(self):
        """
        DESCRIPTION: * Navigate to Sport Landing page > 'In-play' tab
        DESCRIPTION: * Verify counters next to 'Live now' and 'Upcoming events'/'Upcoming' for Desktop
        EXPECTED: * Value in 'Live now' counter corresponds to **liveEventCount** attribute in WS (respective sport item)
        EXPECTED: * Value in 'Upcoming events' counter corresponds to **upcomingEventCount** attribute in WS (respective sport item)
        """
        pass

    def test_006_for_mobiletablet_navigate_to_home_page__in_play_tab_verify_counters_next_to_live_now_see_all_and_upcoming_events(self):
        """
        DESCRIPTION: **For mobile/tablet:**
        DESCRIPTION: * Navigate to Home page > 'In-play' tab
        DESCRIPTION: * Verify counters next to 'Live now See All' and 'Upcoming events'
        EXPECTED: * Value in 'Live now See All' counter corresponds to **liveEventCount** attribute in WS ('All sports' item)
        EXPECTED: * Value in 'Upcoming events' counter corresponds to **upcomingEventCount** attribute in WS ('All sports' item)
        """
        pass
