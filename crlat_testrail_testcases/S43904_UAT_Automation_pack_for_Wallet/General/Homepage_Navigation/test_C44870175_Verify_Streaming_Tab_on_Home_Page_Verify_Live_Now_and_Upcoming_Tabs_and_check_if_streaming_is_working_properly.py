import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.homepage_featured
@vtest
class Test_C44870175_Verify_Streaming_Tab_on_Home_Page_Verify_Live_Now_and_Upcoming_Tabs_and_check_if_streaming_is_working_properly(Common):
    """
    TR_ID: C44870175
    NAME: Verify Streaming Tab on Home Page. Verify Live Now and Upcoming Tabs and check if streaming is working properly.
    DESCRIPTION: "Verify user sees 'Streaming' tab on HP and 'Live Now' , 'upcoming' tabs - Verify 'Live now' page categorise into sports -Verify User can navigate to correct event on both 'Live Now' , 'upcoming' tabs events. - Verify user can check streaming properly
    PRECONDITIONS: User need to logged in in order to watch Live streaming
    """
    keep_browser_open = True

    def test_001_load_app(self):
        """
        DESCRIPTION: Load app
        EXPECTED: App is loaded user is landed on Home Page
        """
        pass

    def test_002_tap_on_live_stream_tab(self):
        """
        DESCRIPTION: Tap on LIVE STREAM TAB
        EXPECTED: Mobile & Tablet : Live Stream page is loaded with LIVE NOW and UPCOMING tabs, LIVE NOW tab expanded by default.
        EXPECTED: Desktop : Live Stream tab displays events with Live streaming available with the highlighted events streaming at the top of the tab.
        """
        pass

    def test_003_click_on_each_sport_category(self):
        """
        DESCRIPTION: Click on each sport category
        EXPECTED: Mobile : User should be able to expand /collapse each sport category and each event.
        EXPECTED: Desktop : user can switch between sports from 'In-Play and Live Stream' carousal.
        """
        pass

    def test_004_click_on_any_event(self):
        """
        DESCRIPTION: Click on any event
        EXPECTED: User should navigate to the corresponding Event Landing Page
        """
        pass

    def test_005_click_back(self):
        """
        DESCRIPTION: Click back
        EXPECTED: User should navigate back to LIVE STREAM tab
        """
        pass

    def test_006_click_on_any_event_and_click_on_watch_icon_at_the_top(self):
        """
        DESCRIPTION: Click on any event and click on WATCH icon at the top
        EXPECTED: User should be able to watch Streaming of the event.
        """
        pass

    def test_007_only_mobile__tablet__verify_upcoming(self):
        """
        DESCRIPTION: Only mobile & Tablet : Verify 'UPCOMING'
        EXPECTED: Upcoming events are listed under this tab categorised by Sport type and sub-categorised by competition type.
        """
        pass

    def test_008_only_mobile__table__repeat_steps_4_5(self):
        """
        DESCRIPTION: Only mobile & Table : repeat steps 4-5
        EXPECTED: 
        """
        pass
