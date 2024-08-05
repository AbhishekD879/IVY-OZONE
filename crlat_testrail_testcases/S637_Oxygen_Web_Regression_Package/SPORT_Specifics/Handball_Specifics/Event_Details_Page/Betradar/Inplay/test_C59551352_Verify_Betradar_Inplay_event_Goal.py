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
class Test_C59551352_Verify_Betradar_Inplay_event_Goal(Common):
    """
    TR_ID: C59551352
    NAME: Verify Betradar Inplay event: Goal
    DESCRIPTION: This test case verifies  that that when there is an incident of  Kick  In in the match Visualization screen displays the  "Goal" text, silk, Player name in the middle and also the Player & Handball position.
    PRECONDITIONS: Navigate to Inplay-> Handball -> Tap on event (which is subscribed to betradar)
    PRECONDITIONS: How to check event is mapped to betradar or not?
    PRECONDITIONS: inspect elements click on inplay event and while loading EDP check for api-key network call. if we get 200 response then event has betradar scoreboard and if we get 404 this event should show fallback
    PRECONDITIONS: Confluence link
    PRECONDITIONS: https://confluence.egalacoral.com/pages/viewpage.action?pageId=139380661
    """
    keep_browser_open = True

    def test_001_navigate_to_the_handball_event_details_page_from_preconditions(self):
        """
        DESCRIPTION: Navigate to the Handball event details page from Preconditions
        EXPECTED: It should navigated to handball EDP
        """
        pass

    def test_002_verify_the_display_of_kick_in_visualization_when_a_team_is_awarded_with_goal(self):
        """
        DESCRIPTION: Verify the display of Kick In visualization when a team is awarded with goal
        EXPECTED: The visualization screen should be displayed with the following :
        EXPECTED: Team & Player Name
        EXPECTED: Silk
        EXPECTED: "Goal" hardcode text
        EXPECTED: Handball ball Position and Court background color should be  blue
        """
        pass
