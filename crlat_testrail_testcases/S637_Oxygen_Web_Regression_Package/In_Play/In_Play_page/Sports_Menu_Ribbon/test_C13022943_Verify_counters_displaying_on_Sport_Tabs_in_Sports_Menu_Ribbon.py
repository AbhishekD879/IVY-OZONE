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

    def test_001_for_mobiletabletverify_counter_displaying_next_to_watch_live_icon(self):
        """
        DESCRIPTION: **For mobile/tablet:**
        DESCRIPTION: Verify Counter displaying next to 'Watch Live' icon
        EXPECTED: Counter is NOT displayed next to 'Watch Live' icon
        """
        pass

    def test_002_for_mobiletablet_select_sport_that_has_both_inplay_and_upcoming_events_verify_counter(self):
        """
        DESCRIPTION: **For mobile/tablet:**
        DESCRIPTION: * Select sport that has both inplay and upcoming events
        DESCRIPTION: * Verify Counter
        EXPECTED: Coral:
        EXPECTED: * Value in Counter corresponds to **liveEventCount** attribute for selected sport
        EXPECTED: * Count of upcoming events is ignored
        EXPECTED: Ladbrokes:
        EXPECTED: * Counter not displayed. "Live" label displayed instead of counter
        """
        pass

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
        pass

    def test_004_for_mobiletablet_select_sport_that_has_only_upcoming_events_verify_counter(self):
        """
        DESCRIPTION: **For mobile/tablet:**
        DESCRIPTION: * Select sport that has ONLY upcoming events
        DESCRIPTION: * Verify Counter
        EXPECTED: Coral:
        EXPECTED: * Counter is not shown
        EXPECTED: Ladbrokes: Counter and Live label not shown
        """
        pass

    def test_005_for_desktop_select_watch_live_tab_gt_live_now_switcher_verify_counter_next_to__watch_live_icon(self):
        """
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: * Select 'Watch Live' tab &gt; 'Live now' switcher
        DESCRIPTION: * Verify Counter next to  'Watch Live' icon
        EXPECTED: Counter is NOT displayed next to 'Watch Live' icon
        """
        pass

    def test_006_for_desktop_select_watch_live_tab_gt_upcoming_switcher_verify_counter_next_to__watch_live_icon(self):
        """
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: * Select 'Watch Live' tab &gt; 'Upcoming' switcher
        DESCRIPTION: * Verify Counter next to  'Watch Live' icon
        EXPECTED: Counter is NOT displayed next to 'Watch Live' icon
        """
        pass

    def test_007_for_desktop_select_any_sport_gt_live_now_switcher_verify_counter_next_to_sport_icon(self):
        """
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: * Select any sport &gt; 'Live now' switcher
        DESCRIPTION: * Verify Counter next to sport icon
        EXPECTED: * Value in Counter corresponds to **liveEventCount** attribute for selected sport
        EXPECTED: * Counter is not shown if sport contains no live events
        """
        pass

    def test_008_for_desktop_select_any_sport_gt_upcoming_switcher_verify_counter_next_to_sport_icon(self):
        """
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: * Select any sport &gt; 'Upcoming' switcher
        DESCRIPTION: * Verify Counter next to sport icon
        EXPECTED: * Value in Counter corresponds to **upcomingEventCount** attribute for selected sport
        EXPECTED: * Counter is not shown if sport contains no upcoming events
        """
        pass
