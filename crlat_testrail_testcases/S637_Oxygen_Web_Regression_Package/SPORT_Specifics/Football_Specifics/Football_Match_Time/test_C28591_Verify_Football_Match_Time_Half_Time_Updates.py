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
class Test_C28591_Verify_Football_Match_Time_Half_Time_Updates(Common):
    """
    TR_ID: C28591
    NAME: Verify Football Match Time/Half Time Updates
    DESCRIPTION: This test case verifies Match Time/Half Time Updates.
    PRECONDITIONS: 1) In order to see match time/half time Football event should be BIP event
    PRECONDITIONS: 2) In order to get events with Scorers use link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Commentary/X.XX/CommentaryForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: Look at the attributes:
    PRECONDITIONS: *   **offset **- match time in seconds on periodCode="FIRST\_HALF/SECOND\_HALF" level
    PRECONDITIONS: *   **periodCode="FIRST_HALF" - **First half of a match/game, **state="S" **(this means that the clock is "stopped")
    PRECONDITIONS: *   **periodCode="SECOND_HALF" - **Second half of a match/game, **state="R" **(this means that the clock is "running")
    PRECONDITIONS: *   **periodCode="HALF_TIME" - **Half time in a match/game, **state="S"**
    PRECONDITIONS: NOTE: UAT assistance is needed in order to generate match time for BIP event.
    PRECONDITIONS: **Match Time updates in real time based on subscription for Live Timer or if it is not available then devise's time should be user as Timer for updating Match Time.**
    """
    keep_browser_open = True

    def test_001_load_invictus_application(self):
        """
        DESCRIPTION: Load Invictus application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_navigate_to_football_landing_page_from_sports_menu_ribbon_mobile_tabletleft_navigation_menu_desktop(self):
        """
        DESCRIPTION: Navigate to Football Landing page from Sports Menu Ribbon (Mobile, Tablet)/Left Navigation menu (Desktop)
        EXPECTED: 'Football' landing page is opened
        """
        pass

    def test_003_clicktap_in_play_tab(self):
        """
        DESCRIPTION: Click/Tap 'In-Play' tab
        EXPECTED: 'In Play' tab is opened
        """
        pass

    def test_004_verify_football_event_with_availablematch_time_for_first_half(self):
        """
        DESCRIPTION: Verify Football event with available Match Time for First Half
        EXPECTED: Event is shown
        """
        pass

    def test_005_verify_match_time(self):
        """
        DESCRIPTION: Verify match time
        EXPECTED: *   Time is running in real time
        EXPECTED: *   Match Time corresponds to an attribute **offset **on periodCode="FIRST_HALF" level
        """
        pass

    def test_006_wait_till_the_end_of_first_half_and_check_timer(self):
        """
        DESCRIPTION: Wait till the end of First Half and check timer
        EXPECTED: Timer is replaced with 'HT' label
        """
        pass

    def test_007_wait_till_the_end_of_half_time_and_check_ht_label(self):
        """
        DESCRIPTION: Wait till the end of Half Time and check 'HT' label
        EXPECTED: 'HT' label is replaced with timer
        """
        pass

    def test_008_verify_match_time(self):
        """
        DESCRIPTION: Verify match time
        EXPECTED: *   Time is running in real time
        EXPECTED: *   Match Time corresponds to an attribute **offset **on periodCode="SECOND_HALF" level
        """
        pass

    def test_009_verify_match_time_for_section_in_a_collapsed_state(self):
        """
        DESCRIPTION: Verify Match Time for section in a collapsed state
        EXPECTED: If section was in collapsed state, after expanding - updated timer will be shown there with correct Match Time or 'HT' label (if it is Half Time now)
        """
        pass

    def test_010_verify_match_time_before_bip_page_is_opened(self):
        """
        DESCRIPTION: Verify Match Time before BIP page is opened
        EXPECTED: If page was opened, user navigated to other page and returned to verified event - updated timer will be shown there with correct Match Time or 'HT' label (if it is Half Time now)
        """
        pass

    def test_011_verify_match_time_after_turned_off_phone_to_sleep_mode(self):
        """
        DESCRIPTION: Verify Match Time after turned off phone to sleep mode
        EXPECTED: If phone was turned off to sleep mode and turned on again, updated timer will be shown there with correct Match Time or 'HT' label (if it is Half Time now)
        """
        pass

    def test_012_navigate_to_in_play_page_from_sports_menu_ribbon_mobile_tabletleft_navigation_menu_desktop(self):
        """
        DESCRIPTION: Navigate to In-Play page from Sports Menu Ribbon (Mobile, Tablet)/Left Navigation menu (Desktop)
        EXPECTED: 'In-Play' tab is shown with 'All Sport' selected
        """
        pass

    def test_013_repeat_steps_4_11(self):
        """
        DESCRIPTION: Repeat steps №4-11
        EXPECTED: 
        """
        pass

    def test_014_clicktap_football_icon_from_the_sports_menu_ribbon_on_in_play_page(self):
        """
        DESCRIPTION: Click/Tap 'Football' icon from the Sports Menu Ribbon on 'In-Play' page
        EXPECTED: 'Football' page is opened
        """
        pass

    def test_015_repeat_steps_4_11(self):
        """
        DESCRIPTION: Repeat steps №4-11
        EXPECTED: 
        """
        pass

    def test_016_navigate_to_live_stream_page_from_sports_menu_ribbon_mobile_tabletleft_navigation_menu_desktop(self):
        """
        DESCRIPTION: Navigate to 'Live Stream' page from Sports Menu Ribbon (Mobile, Tablet)/Left Navigation menu (Desktop)
        EXPECTED: 'Live Stream' page is opened
        """
        pass

    def test_017_repeat_steps_4_11(self):
        """
        DESCRIPTION: Repeat steps №4-11
        EXPECTED: 
        """
        pass

    def test_018_clicktap_live_stream_tab_on_the_module_selector_ribbon_on_the_homepage(self):
        """
        DESCRIPTION: Click/Tap 'Live Stream' tab on the Module Selector Ribbon on the Homepage
        EXPECTED: 'Live Stream' tab is opened
        """
        pass

    def test_019_repeat_steps_4_11(self):
        """
        DESCRIPTION: Repeat steps №4-11
        EXPECTED: 
        """
        pass

    def test_020_clicktap_in_play_tab_on_the_module_selector_ribbon_on_the_homepage(self):
        """
        DESCRIPTION: Click/Tap 'In-Play' tab on the Module Selector Ribbon on the Homepage
        EXPECTED: 'In-Play' tab is opened
        """
        pass

    def test_021_repeat_steps_4_11(self):
        """
        DESCRIPTION: Repeat steps №4-11
        EXPECTED: 
        """
        pass

    def test_022_for_desktopnavigate_to_sports_landing_page_and_make_sure_that_in_play_widget_with_live_events_is_available(self):
        """
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: Navigate to Sports Landing page and make sure that 'In-Play' widget with live events is available
        EXPECTED: 'In-Play' widget is present and contains live events
        """
        pass

    def test_023_repeat_steps_4_11(self):
        """
        DESCRIPTION: Repeat steps №4-11
        EXPECTED: 
        """
        pass

    def test_024_for_desktopnavigate_to_sports_landing_page_and_make_sure_that_live_stream_widget_is_available(self):
        """
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: Navigate to Sports Landing page and make sure that 'Live Stream 'widget is available
        EXPECTED: 'Live Stream' widget is present
        """
        pass

    def test_025_repeat_steps_4_11(self):
        """
        DESCRIPTION: Repeat steps №4-11
        EXPECTED: 
        """
        pass
