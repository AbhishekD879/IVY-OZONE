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
class Test_C333898_Verify_Live_now_and_Upcoming_counters_updating(Common):
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

    def test_001_in_ti_undisplayset_results_to_any_events_from_watch_live_tab_gt_live_now_and_upcoming_events_sectionswitchernoteattribute_displayedn_should_be_set_for_event_(self):
        """
        DESCRIPTION: In TI undisplay/set results to any events from 'Watch live' tab &gt; 'Live now' and 'Upcoming events' section/switcher
        DESCRIPTION: NOTE:
        DESCRIPTION: (attribute 'displayed="N"' should be set for event )
        EXPECTED: * Undisplayed/resulted event is removed from front-end automatically
        EXPECTED: * Counter next 'Live now' and 'Upcoming events' section/switcher is updated
        EXPECTED: * Updated value in Counter corresponds to **liveStreamEventCount** and ** upcomingLiveStreamEventCount**attribute in WS ('All sports' item)
        """
        pass

    def test_002_trigger_starting_of_inplay_and_upcoming_events_with_streaming_mapped(self):
        """
        DESCRIPTION: Trigger starting of inplay and upcoming events with streaming mapped
        EXPECTED: * Started events appear on front-end automatically
        EXPECTED: * Counter next 'Live now' and 'Upcoming events' section/switcher is updated
        EXPECTED: * Updated value in Counter corresponds to **liveStreamEventCount** and ** upcomingLiveStreamEventCount**attribute in WS ('All sports' item)
        """
        pass

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
        pass

    def test_004_trigger_starting_of_inplay_and_upcoming_events_for_the_same_sport(self):
        """
        DESCRIPTION: Trigger starting of inplay and upcoming events for the same sport
        EXPECTED: * Started events appear on front-end automatically
        EXPECTED: * Counter next 'Live now' and 'Upcoming events' section/switcher is updated
        EXPECTED: * Updated value in Counter corresponds to **liveEventCount** and ** upcomingEventCount**attribute in WS (respective sport item)
        """
        pass

    def test_005__navigate_to_sport_landing_page_gt_in_play_tab_in_ti_undisplayset_results_to_any_inplay_and_upcoming_events_from_selected_sportnoteattribute_displayedn_should_be_set_for_event_(self):
        """
        DESCRIPTION: * Navigate to Sport Landing page &gt; 'In-play' tab
        DESCRIPTION: * In TI undisplay/set results to any inplay and upcoming events from selected sport
        DESCRIPTION: NOTE:
        DESCRIPTION: (attribute 'displayed="N"' should be set for event )
        EXPECTED: * Undisplayed/resulted event is removed from front-end automatically
        EXPECTED: * Counter next 'Live now' and 'Upcoming events' section/switcher is updated
        EXPECTED: * Updated value in Counter corresponds to **liveEventCount** and ** upcomingEventCount**attribute in WS (respective sport item)
        """
        pass

    def test_006_trigger_starting_of_inplay_and_upcoming_events_for_the_same_sport(self):
        """
        DESCRIPTION: Trigger starting of inplay and upcoming events for the same sport
        EXPECTED: * Started events appear on front-end automatically
        EXPECTED: * Counter next 'Live now' and 'Upcoming events' section/switcher is updated
        EXPECTED: * Updated value in Counter corresponds to **liveEventCount** and ** upcomingEventCount**attribute in WS (respective sport item)
        """
        pass

    def test_007_for_mobiletablet_navigate_to_home_page_gt_in_play_tab_in_ti_undisplayset_results_to_any_inplay_and_upcoming_events(self):
        """
        DESCRIPTION: **For mobile/tablet:**
        DESCRIPTION: * Navigate to Home page &gt; 'In-play' tab
        DESCRIPTION: * In TI undisplay/set results to any inplay and upcoming events
        EXPECTED: * Undisplayed/resulted event is removed from front-end automatically
        EXPECTED: * Counter next 'Live now See All' and 'Upcoming events' sections is updated
        EXPECTED: * Updated value in Counter corresponds to **liveEventCount** and ** upcomingEventCount**attribute in WS ('All sports' item)
        """
        pass

    def test_008_for_mobiletablettrigger_starting_of_any_inplay_and_upcoming_events(self):
        """
        DESCRIPTION: **For mobile/tablet:**
        DESCRIPTION: Trigger starting of any inplay and upcoming events
        EXPECTED: * Started events appear on front-end automatically
        EXPECTED: * Counter next 'Live now See All' and 'Upcoming events' sections is updated
        EXPECTED: * Updated value in Counter corresponds to **liveEventCount** and ** upcomingEventCount**attribute in WS ('All sports' item)
        """
        pass
