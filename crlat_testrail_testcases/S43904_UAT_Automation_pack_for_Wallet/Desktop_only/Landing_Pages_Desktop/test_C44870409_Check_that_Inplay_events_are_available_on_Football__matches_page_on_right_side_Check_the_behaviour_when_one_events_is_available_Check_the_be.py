import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C44870409_Check_that_Inplay_events_are_available_on_Football__matches_page_on_right_side_Check_the_behaviour_when_one_events_is_available_Check_the_behaviour_when_multiple_events_are_available_and_user_can_scroll_thr_all_of_them_Check_user_can_expand_an(Common):
    """
    TR_ID: C44870409
    NAME: "Check that Inplay events are available on Football -> matches page on right side  Check the behaviour when one events is available  Check the behaviour when multiple events are available and user can scroll thr' all of them  Check user can expand an
    DESCRIPTION: "Check that Inplay events are available on Football -> matches page on right side
    DESCRIPTION: Check the behaviour when one events is available
    DESCRIPTION: Check the behaviour when multiple events are available and user can scroll thr' all of them
    DESCRIPTION: Check user can expand and collapse the section
    DESCRIPTION: Check user can navigate to In play page on click of link available below section
    DESCRIPTION: Check event details are correct on section with odds and score if applicable
    DESCRIPTION: CHeck all the details are updating with PUSH
    DESCRIPTION: Check all above steps on multiple sports say Tennis, Basketball
    DESCRIPTION: - Verify 'Live now' and 'Upcoming Events' counters on In-play page when move to mode on Desktop (updated counters should be shown after unlocking)
    DESCRIPTION: "
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_launch_the_application(self):
        """
        DESCRIPTION: Launch the Application
        EXPECTED: Application should be launched
        """
        pass

    def test_002_navigate_to_football_page(self):
        """
        DESCRIPTION: Navigate to Football page
        EXPECTED: User should be navigated to the Football landing page with the Inplay, matches, competitions,accumulators, outrights and Specials tab
        """
        pass

    def test_003_verify_the_user_can_expand_and_collapse_the_section(self):
        """
        DESCRIPTION: Verify the user can expand and collapse the section
        EXPECTED: User should be able to expand or collapse
        """
        pass

    def test_004_verify_the_user_can_navigate_to_inplay_page_on_click_of_link_available_below_section(self):
        """
        DESCRIPTION: Verify the user can navigate to Inplay page on click of link available below section
        EXPECTED: user should be navigated to the inplay section
        """
        pass

    def test_005_verify_the_event_details_are_correct_on_the_section_with_odds_and_score_if_applicableverify_the_all_the_details_are_updating_with_push(self):
        """
        DESCRIPTION: Verify the event details are correct on the section with odds and score if applicable
        DESCRIPTION: Verify the all the details are updating with PUSH
        EXPECTED: Event details with the odds (score if available) should be displayed
        """
        pass

    def test_006_verify_live_now_and_upcoming_events_counters_on_in_play_page_when_move_to_mode_on_desktop(self):
        """
        DESCRIPTION: Verify 'Live now' and 'Upcoming Events' counters on In-play page when move to mode on Desktop
        EXPECTED: Live now' and 'Upcoming Events' sections should be displayed under In-play tab.
        """
        pass
