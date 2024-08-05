import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.sports
@vtest
class Test_C28589_Verify_Match_Time_Displaying(Common):
    """
    TR_ID: C28589
    NAME: Verify Match Time Displaying
    DESCRIPTION: This test case verifies match time of BIP events.
    PRECONDITIONS: 1) In order to see match time Football event should be BIP event
    PRECONDITIONS: 2) In order to get events with Scorers use link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Commentary/X.XX/CommentaryForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: Look at the attributes:
    PRECONDITIONS: *   **offset **- match time in seconds on periodCode="FIRST\_HALF/SECOND\_HALF" level
    PRECONDITIONS: *   **periodCode="FIRST_HALF" - **First half of a match/game, **state="S" **(this means that the clock is "stopped")
    PRECONDITIONS: *   **periodCode="SECOND_HALF" - **Second half of a match/game, **state="R" **(this means that the clock is "running")
    PRECONDITIONS: NOTE: UAT assistance is needed in order to generate match time for BIP event.
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_for_mobiletabletnavigate_to_football_landing_page_from_the_sports_menu_ribbonfor_desktopnavigate_to_football_landing_page_from_the_left_navigation_menu(self):
        """
        DESCRIPTION: **For Mobile/Tablet:**
        DESCRIPTION: Navigate to 'Football' Landing page from the Sports Menu Ribbon
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: Navigate to 'Football' Landing page from the 'Left Navigation' menu
        EXPECTED: 'Football' landing page is opened
        """
        pass

    def test_003_clicktap_in_play_tab(self):
        """
        DESCRIPTION: Click/Tap 'In-Play' tab
        EXPECTED: 'In-Play' tab is opened
        """
        pass

    def test_004_verify_football_event_with_match_time_available(self):
        """
        DESCRIPTION: Verify Football event with Match Time available
        EXPECTED: Event is shown
        """
        pass

    def test_005_verify_match_time_displaying(self):
        """
        DESCRIPTION: Verify Match Time displaying
        EXPECTED: Match time is shown below the Sport icon instead of Start Time in format:
        EXPECTED: **MM** (minutes only)
        """
        pass

    def test_006_verify_match_time_correctness(self):
        """
        DESCRIPTION: Verify Match Time correctness
        EXPECTED: *   Match Time corresponds to an attribute **offset **on active periodCode level:
        EXPECTED: periodCode="FIRST\_HALF" (if it is first half now) or periodCode="SECOND\_HALF" (if it is second half now)
        EXPECTED: *   **offset **in seconds **/ 60 = ****offset **in minutes (only value before comma is taken into consideration)
        """
        pass

    def test_007_verify_match_time_for_outright_events(self):
        """
        DESCRIPTION: Verify Match Time for Outright events
        EXPECTED: Match Time is not shown for Outright events
        EXPECTED: The Sports icon is displayed only
        """
        pass

    def test_008_find_event_from_step_4_and_repeat_steps_5_6(self):
        """
        DESCRIPTION: Find event from step №4 and repeat steps №5-6
        EXPECTED: 
        """
        pass

    def test_009_navigate_to_the_homepage(self):
        """
        DESCRIPTION: Navigate to the Homepage
        EXPECTED: Homepage is opened
        """
        pass

    def test_010_for_mobiletabletnavigate_to_in_play_page_from_the_sports_menu_ribbonfor_desktopnavigate_to_in_play_page_from_the_main_navigation_menu_at_the_universal_header(self):
        """
        DESCRIPTION: **For Mobile/Tablet:**
        DESCRIPTION: Navigate to 'In-Play' page from the Sports Menu Ribbon
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: Navigate to 'In-Play' page from the 'Main Navigation' menu at the 'Universal Header'
        EXPECTED: 'In-Play' tab is shown with 'All Sport' selected
        """
        pass

    def test_011_repeat_steps_4_7(self):
        """
        DESCRIPTION: Repeat steps №4-7
        EXPECTED: 
        """
        pass

    def test_012_clicktap_football_icon_from_the_sports_menu_ribbon_on_in_play_page(self):
        """
        DESCRIPTION: Click/Tap 'Football' icon from the Sports Menu Ribbon on 'In-Play' page
        EXPECTED: 'Football' page is opened
        """
        pass

    def test_013_repeat_steps_4_7(self):
        """
        DESCRIPTION: Repeat steps №4-7
        EXPECTED: 
        """
        pass

    def test_014_for_mobiletabletnavigate_to_live_stream_page_from_the_sports_menu_ribbonfor_desktopnavigate_to_live_stream_page_from_the_main_navigation_menu_at_the_universal_header(self):
        """
        DESCRIPTION: **For Mobile/Tablet:**
        DESCRIPTION: Navigate to 'Live Stream' page from the Sports Menu Ribbon
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: Navigate to 'Live Stream' page from the 'Main Navigation' menu at the 'Universal Header'
        EXPECTED: 'Live Stream' page is opened
        """
        pass

    def test_015_repeat_steps_4_7(self):
        """
        DESCRIPTION: Repeat steps №4-7
        EXPECTED: 
        """
        pass

    def test_016_for_mobiletablettap_in_play_tab_on_the_module_selector_ribbon_on_the_homepage(self):
        """
        DESCRIPTION: **For Mobile/Tablet:**
        DESCRIPTION: Tap 'In-Play' tab on the Module Selector Ribbon on the Homepage
        EXPECTED: **For Mobile/Tablet:**
        EXPECTED: 'In-Play' tab is opened
        """
        pass

    def test_017_for_mobiletabletrepeat_steps_4_7(self):
        """
        DESCRIPTION: **For Mobile/Tablet:**
        DESCRIPTION: Repeat steps №4-7
        EXPECTED: 
        """
        pass

    def test_018_for_mobiletablettap_live_stream_tab_on_the_module_selector_ribbon_on_the_homepage(self):
        """
        DESCRIPTION: **For Mobile/Tablet:**
        DESCRIPTION: Tap 'Live Stream' tab on the Module Selector Ribbon on the Homepage
        EXPECTED: **For Mobile/Tablet:**
        EXPECTED: 'Live Stream' tab is opened
        """
        pass

    def test_019_for_mobiletabletrepeat_steps_4_7(self):
        """
        DESCRIPTION: **For Mobile/Tablet:**
        DESCRIPTION: Repeat steps №4-7
        EXPECTED: 
        """
        pass

    def test_020_for_desktopnavigate_to_in_play__live_stream_section_at_the_homepage_by_scrolling_the_page_down(self):
        """
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: Navigate to 'In-Play & Live Stream ' section at the Homepage by scrolling the page down
        EXPECTED: **For Desktop:**
        EXPECTED: * 'In-Play' Landing Page is opened
        EXPECTED: * The first 'Sport' tab is selected by default
        EXPECTED: * Two switchers are visible: 'In-Play' and 'Live Stream'
        """
        pass

    def test_021_for_desktoprepeat_steps_4_7(self):
        """
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: Repeat steps №4-7
        EXPECTED: 
        """
        pass

    def test_022_for_desktopchoose_live_stream_switcher(self):
        """
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: Choose 'Live Stream' switcher
        EXPECTED: **For Desktop:**
        EXPECTED: * 'Live Stream' Landing Page is opened
        EXPECTED: * 'Live Stream' is selected
        """
        pass

    def test_023_for_desktoprepeat_steps_4_7(self):
        """
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: Repeat steps №4-7
        EXPECTED: 
        """
        pass

    def test_024_for_desktopnavigate_to_sports_landing_page_and_make_sure_that_in_play_widget_with_live_events_is_available(self):
        """
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: Navigate to Sports Landing page and make sure that 'In-Play' widget with live events is available
        EXPECTED: 'In-Play' widget is present and contains live events
        """
        pass

    def test_025_repeat_steps_4_7(self):
        """
        DESCRIPTION: Repeat steps №4-7
        EXPECTED: 
        """
        pass

    def test_026_for_desktopnavigate_to_sports_landing_page_and_make_sure_that_live_stream_widget_is_available(self):
        """
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: Navigate to Sports Landing page and make sure that 'Live Stream 'widget is available
        EXPECTED: 'Live Stream' widget is present
        """
        pass

    def test_027_repeat_steps_4_7(self):
        """
        DESCRIPTION: Repeat steps №4-7
        EXPECTED: 
        """
        pass
