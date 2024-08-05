import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C59551334_Verify_Betradar_Inplay_event_End_of_the_Match(Common):
    """
    TR_ID: C59551334
    NAME: Verify Betradar Inplay event: End of the Match
    DESCRIPTION: This test case verifies display of score board once the event has been ended
    PRECONDITIONS: Navigate to Inplay-> Handball -> Tap on event (which is subscribed to betradar)
    PRECONDITIONS: How to check event is mapped to betradar or not?
    PRECONDITIONS: inspect elements click on inplay event and while loading EDP check for api-key network call. if we get 200 response then event has betradar scoreboard and if we get 404 this event should show fallback
    PRECONDITIONS: Confluence link
    PRECONDITIONS: https://confluence.egalacoral.com/pages/viewpage.action?pageId=139380661
    """
    keep_browser_open = True

    def test_001_navigate_to_the_fustal_event_details_page_from_preconditions(self):
        """
        DESCRIPTION: Navigate to the Fustal event details page from Preconditions
        EXPECTED: It should navigated to Fustal EDP
        """
        pass

    def test_002_verify_the_visualization_of_bet_radar_scoreboard_screen_once_the_event_has_been_finished(self):
        """
        DESCRIPTION: Verify the visualization of bet radar scoreboard screen once the event has been finished
        EXPECTED: The visualization screen should be displayed with the following details:
        EXPECTED: Event ended time
        EXPECTED: Match Ended hard code text
        EXPECTED: Both teams score
        EXPECTED: Event Name and details
        """
        pass
