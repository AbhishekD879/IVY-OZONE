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
class Test_C28665_Verify_Tennis_Live_Scores_Displaying_when_New_Set_appears(Common):
    """
    TR_ID: C28665
    NAME: Verify Tennis Live Scores Displaying when New Set appears
    DESCRIPTION: This test case verifies live scores displaying when new set appears.
    DESCRIPTION: NOTE: UAT assistance is needed for LIVE Scores changing. ([or use instruction][1])
    DESCRIPTION: [1]: https://confluence.egalacoral.com/display/MOB/How+to+generate+Live+Score+updates+on+Tennis+and+Football+sports
    PRECONDITIONS: 1) In order to have a Scores Tennis event should be BIP event
    PRECONDITIONS: 2) In order to get events with Scorers use link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Commentary/X.XX/CommentaryForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: Look at the attributes:
    PRECONDITIONS: *   **eventParticipantID** -  to verify player name and corresponding player score
    PRECONDITIONS: *   **periodCode**='GAME', **description**="Game in Tennis match', **state**='R/S', periodIndex="X" with the highest value  - to look at the scorers for the full match
    PRECONDITIONS: *   **periodCode**="SET", **description**="Set in Tennis match", periodIndex="X" - to look at the scorers for the specific Set (where X-set number)
    PRECONDITIONS: *   **state**='R' - set in running state
    PRECONDITIONS: *   **state**='S' - set in stopped state
    PRECONDITIONS: *   **factCode**='SCORE' &** name**='Score of the match/game' - to see Match facts
    PRECONDITIONS: *   **'fact'** - to see a score for particular participant
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_for_mobiletabletnavigate_to_tennis_landing_page_from_the_sports_menu_ribbonfor_desktopnavigate_to_tennis_landing_page_from_the_left_navigation_menu(self):
        """
        DESCRIPTION: **For Mobile/Tablet:**
        DESCRIPTION: Navigate to 'Tennis' Landing page from the Sports Menu Ribbon
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: Navigate to 'Tennis' Landing page from the 'Left Navigation' menu
        EXPECTED: 'Tennis' landing page is opened
        """
        pass

    def test_003_clicktap_in_play_tab(self):
        """
        DESCRIPTION: Click/Tap 'In-Play' tab
        EXPECTED: 'In-Play' tab is opened
        """
        pass

    def test_004_verify_tennis_event_with_score_available(self):
        """
        DESCRIPTION: Verify Tennis event with score available
        EXPECTED: Each score for particular player is shown in the same row as player's name near the Price/Odds button
        """
        pass

    def test_005_trigger_the_following_situationnew_set_appears(self):
        """
        DESCRIPTION: Trigger the following situation:
        DESCRIPTION: **New set appears**
        EXPECTED: *   Score for new set immediately appears
        EXPECTED: *   Number of set below the sport icon is increased by one set (e.g.'1st Set' is changed to '2nd Set', '2nd Set' is changed to '3rd Set')
        """
        pass

    def test_006_verify_new_set_appearing_for_sections_in_a_collapsed_state(self):
        """
        DESCRIPTION: Verify new set appearing for sections in a collapsed state
        EXPECTED: If section is collapsed and new set appears, after expanding the section - score of new set and updated number of sets will be shown there
        """
        pass

    def test_007_verify_new_set_appearing_before_application_is_opened(self):
        """
        DESCRIPTION: Verify new set appearing before application is opened
        EXPECTED: If application was not started/opened and new set appears, after opening application and verified event - score of new set and updated set number will be shown there
        """
        pass

    def test_008_verify_new_set_appearing_when_details_page_of_verified_event_is_opened(self):
        """
        DESCRIPTION: Verify new set appearing when Details Page of verified event is opened
        EXPECTED: After tapping Back button score of new set and updated set number will be shown on Landing page
        """
        pass

    def test_009_for_mobiletabletnavigate_to_in_play_page_from_the_sports_menu_ribbonfor_desktopnavigate_to_in_play_page_from_the_main_navigation_menu_at_the_universal_header(self):
        """
        DESCRIPTION: **For Mobile/Tablet:**
        DESCRIPTION: Navigate to 'In-Play' page from the Sports Menu Ribbon
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: Navigate to 'In-Play' page from the 'Main Navigation' menu at the 'Universal Header'
        EXPECTED: 'In-Play' page is shown with 'All Sport' tab selected
        """
        pass

    def test_010_repeat_steps_4_8(self):
        """
        DESCRIPTION: Repeat steps №4-8
        EXPECTED: 
        """
        pass

    def test_011_clicktap_tennis_icon_from_the_sports_menu_ribbon_on_in_play_page(self):
        """
        DESCRIPTION: Click/Tap 'Tennis' icon from the Sports Menu Ribbon on 'In-Play' page
        EXPECTED: 'Tennis' page is opened
        """
        pass

    def test_012_repeat_steps_4_8(self):
        """
        DESCRIPTION: Repeat steps №4-8
        EXPECTED: 
        """
        pass

    def test_013_for_mobiletabletnavigate_to_live_stream_page_from_the_sports_menu_ribbonfor_desktopnavigate_to_live_stream_page_from_the_main_navigation_menu_at_the_universal_header(self):
        """
        DESCRIPTION: **For Mobile/Tablet:**
        DESCRIPTION: Navigate to 'Live Stream' page from the Sports Menu Ribbon
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: Navigate to 'Live Stream' page from the 'Main Navigation' menu at the 'Universal Header'
        EXPECTED: 'Live Stream' page is opened
        """
        pass

    def test_014_repeat_steps_4_8(self):
        """
        DESCRIPTION: Repeat steps №4-8
        EXPECTED: 
        """
        pass

    def test_015_for_mobiletablettap_in_play_tab_from_the_module_selector_ribbon_on_the_homepage(self):
        """
        DESCRIPTION: **For Mobile/Tablet:**
        DESCRIPTION: Tap 'In-Play' tab from the Module Selector Ribbon on the Homepage
        EXPECTED: **For Mobile/Tablet:**
        EXPECTED: 'In-Play' tab is opened
        """
        pass

    def test_016_for_mobiletabletrepeat_steps_4_8(self):
        """
        DESCRIPTION: **For Mobile/Tablet:**
        DESCRIPTION: Repeat steps №4-8
        EXPECTED: 
        """
        pass

    def test_017_for_mobiletablettap_live_stream_tab_on_the_module_selector_ribbon_on_the_homepage(self):
        """
        DESCRIPTION: **For Mobile/Tablet:**
        DESCRIPTION: Tap 'Live Stream' tab on the Module Selector Ribbon on the Homepage
        EXPECTED: **For Mobile/Tablet:**
        EXPECTED: 'Live Stream' tab is opened
        """
        pass

    def test_018_for_mobiletabletrepeat_steps_4_8(self):
        """
        DESCRIPTION: **For Mobile/Tablet:**
        DESCRIPTION: Repeat steps №4-8
        EXPECTED: 
        """
        pass

    def test_019_for_desktopnavigate_to_in_play__live_stream_section_at_the_homepage_by_scrolling_the_page_down(self):
        """
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: Navigate to 'In-Play & Live Stream ' section at the Homepage by scrolling the page down
        EXPECTED: **For Desktop:**
        EXPECTED: * 'In-Play' Landing Page is opened
        EXPECTED: * The first 'Sport' tab is selected by default
        EXPECTED: * Two switchers are visible: 'In-Play' and 'Live Stream'
        """
        pass

    def test_020_for_desktoprepeat_steps_4_8(self):
        """
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: Repeat steps №4-8
        EXPECTED: 
        """
        pass

    def test_021_for_desktopchoose_live_stream_switcher(self):
        """
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: Choose 'Live Stream' switcher
        EXPECTED: **For Desktop:**
        EXPECTED: * 'Live Stream' Landing Page is opened
        EXPECTED: * 'Live Stream' is selected
        """
        pass

    def test_022_for_desktoprepeat_steps_4_8(self):
        """
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: Repeat steps №4-8
        EXPECTED: 
        """
        pass

    def test_023_for_desktopnavigate_to_sports_landing_page_and_make_sure_that_in_play_widget_with_live_events_is_available(self):
        """
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: Navigate to Sports Landing page and make sure that 'In-Play' widget with live events is available
        EXPECTED: 'In-Play' widget is present and contains live events
        """
        pass

    def test_024_repeat_steps_4_8(self):
        """
        DESCRIPTION: Repeat steps №4-8
        EXPECTED: 
        """
        pass

    def test_025_for_desktopnavigate_to_sports_landing_page_and_make_sure_that_live_stream_widget_is_available(self):
        """
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: Navigate to Sports Landing page and make sure that 'Live Stream 'widget is available
        EXPECTED: 'Live Stream' widget is present
        """
        pass

    def test_026_repeat_steps_4_8(self):
        """
        DESCRIPTION: Repeat steps №4-8
        EXPECTED: 
        """
        pass
