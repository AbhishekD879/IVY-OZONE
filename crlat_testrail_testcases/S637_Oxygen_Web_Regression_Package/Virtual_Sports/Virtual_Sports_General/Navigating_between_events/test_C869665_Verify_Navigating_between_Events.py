import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.virtual_sports
@vtest
class Test_C869665_Verify_Navigating_between_Events(Common):
    """
    TR_ID: C869665
    NAME: Verify Navigating between Events
    DESCRIPTION: This test case verifies navigating between events using 'Next', 'Prev' buttons
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_go_to_virtual_sports(self):
        """
        DESCRIPTION: Go to 'Virtual Sports'
        EXPECTED: Virtual Sports successfully opened
        EXPECTED: Next or current event is shown
        """
        pass

    def test_002_verify_the_page(self):
        """
        DESCRIPTION: Verify the page
        EXPECTED: Video streaming section is expanded
        EXPECTED: First market section is expanded, the rest (if any) are collapsed by default
        """
        pass

    def test_003_navigate_to_different_events_within_this_sport_using_event_selector(self):
        """
        DESCRIPTION: Navigate to different events within this sport using event selector
        EXPECTED: User is able to navigate to different event details pages of the same sport
        """
        pass

    def test_004_verify_events_information(self):
        """
        DESCRIPTION: Verify events' information
        EXPECTED: Events' information is displayed accordingly to selected event
        """
        pass

    def test_005_collapseexpand_sections_with_markets_and_navigate_between_events(self):
        """
        DESCRIPTION: Collapse/expand sections with markets and navigate between events
        EXPECTED: State of expanded/collapsed sections with markets is saved during navigation between different events
        """
        pass

    def test_006_repeat_this_test_case_for_the_following_virtual_sports_greyhounds_football_motorsports_cycling_speedway_tennis_grand_national(self):
        """
        DESCRIPTION: Repeat this test case for the following virtual sports:
        DESCRIPTION: * Greyhounds
        DESCRIPTION: * Football,
        DESCRIPTION: * Motorsports,
        DESCRIPTION: * Cycling,
        DESCRIPTION: * Speedway,
        DESCRIPTION: * Tennis,
        DESCRIPTION: * Grand National
        EXPECTED: 
        """
        pass
