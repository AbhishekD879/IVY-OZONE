import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.in_play
@vtest
class Test_C2745984_Verify_Watch_live_page_in_In_Play_sports_ribbon(Common):
    """
    TR_ID: C2745984
    NAME: Verify 'Watch live' page in In-Play sports ribbon
    DESCRIPTION: This test case verifies "Watch live" page in In-Play sports ribbon
    DESCRIPTION: Note: cannot automate, we won't be undisplaying events because it might affect other testers and tests.
    PRECONDITIONS: 1. "Watch Live" module should be enabled in CMS-> System Configuration ->InPlayWatchLive
    PRECONDITIONS: 2. There should be events with/without mapped streams(both live and upcoming events ) preconfigured for current and upcoming dates.
    PRECONDITIONS: 3. Login to Oxygen app and navigate to "In-PLay" tab
    """
    keep_browser_open = True

    def test_001_verify_displaying_of_watch_live_icon_in_play_sports_ribbon_tab(self):
        """
        DESCRIPTION: Verify displaying of "Watch Live" icon In-Play Sports Ribbon tab
        EXPECTED: * "Watch Live" icon is displayed as the FIRST icon in the ribbon
        """
        pass

    def test_002_verify_default_users_navigation_after_in_play_tab_opening(self):
        """
        DESCRIPTION: Verify default user's navigation after In-Play tab opening
        EXPECTED: * The user is landed on the **FIRST SPORT** (e.g. Football) in the ribbon by default (not the Watch Live tab)
        """
        pass

    def test_003_click_on_watch_live_iconverify_displaying_of_events_with_mapped_streams_in_live_now_and_upcoming_events_sections(self):
        """
        DESCRIPTION: Click on "Watch Live" icon
        DESCRIPTION: Verify displaying of events with mapped streams in **LIVE NOW** and **UPCOMING EVENTS** sections
        EXPECTED: * "Watch Live" page is opened
        EXPECTED: * **LIVE NOW** and **UPCOMING EVENTS** sections are displayed
        EXPECTED: * Events with attribute 'isStarted="true"' are displayed in **LIVE NOW** section
        EXPECTED: * Events which are not started are displayed in **UPCOMING EVENTS** section
        EXPECTED: * Events without available stream are not displayed in "Watch live" page
        """
        pass

    def test_004_go_to_ti_and_undisplay_all_events_from_live_now_tab(self):
        """
        DESCRIPTION: Go to TI and undisplay all events from **LIVE NOW** tab.
        EXPECTED: 
        """
        pass

    def test_005_go_to_app__in_play_tab_watch_live_icon___live_now_section_and_verify_displaying_of_events(self):
        """
        DESCRIPTION: GO to app-> In-Play tab->"Watch Live" icon -> **LIVE NOW** section and verify displaying of events
        EXPECTED: * "Watch Live" page is opened
        EXPECTED: * **LIVE NOW** and upcoming sections are displayed
        EXPECTED: * No events are displayed in **LIVE NOW** section
        EXPECTED: * "There are currently no Live events available" text is displayed in **LIVE NOW** section
        """
        pass

    def test_006_scroll_to_upcoming_events_section_and_verify_displaying_of_upcoming_events(self):
        """
        DESCRIPTION: Scroll to **UPCOMING EVENTS** section and verify displaying of upcoming events
        EXPECTED: * All upcoming events with available Streams are displayed in **UPCOMING EVENTS** section
        """
        pass

    def test_007_go_to_ti_and_undisplay_all_events_from_upcoming_events_section(self):
        """
        DESCRIPTION: Go to TI and undisplay all events from **UPCOMING EVENTS** section.
        EXPECTED: 
        """
        pass

    def test_008_go_to_app__in_play_tab_watch_live_icon__upcoming_events_section_and_verify_displaying_of_events(self):
        """
        DESCRIPTION: GO to app-> In-Play tab->"Watch Live" icon-> **UPCOMING EVENTS** section and verify displaying of events
        EXPECTED: * "Watch Live" page is opened
        EXPECTED: * **LIVE NOW** and **UPCOMING EVENTS** sections are displayed
        EXPECTED: * No events are displayed in **UPCOMING EVENTS** section
        EXPECTED: * "There are no upcoming events" text is displayed in **UPCOMING EVENTS** section
        """
        pass
