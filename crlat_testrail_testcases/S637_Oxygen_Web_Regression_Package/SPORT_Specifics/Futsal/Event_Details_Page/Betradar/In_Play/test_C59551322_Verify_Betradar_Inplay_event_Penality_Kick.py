import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.navigation
@vtest
class Test_C59551322_Verify_Betradar_Inplay_event_Penality_Kick(Common):
    """
    TR_ID: C59551322
    NAME: Verify Betradar Inplay event: Penality Kick
    DESCRIPTION: This test case verifies that when there is an incident of Penalty Kick in the match Visualization screen displays the  "Penalty Kick" text, silk, Player name in the middle and also the Player & Futsal ball position.
    PRECONDITIONS: Navigate to Inplay-> Futsal -> Tap on event (which is subscribed to betradar)
    PRECONDITIONS: How to check event is mapped to betradar or not?
    PRECONDITIONS: inspect elements click on inplay event and while loading EDP check for api-key network call. if we get 200 response then event has betradar and if we get 404 this event should show fallback
    PRECONDITIONS: Confluence link:
    PRECONDITIONS: https://confluence.egalacoral.com/pages/viewpage.action?pageId=139380661
    """
    keep_browser_open = True

    def test_001_navigate_to_the_fustal_event_details_page_from_preconditions(self):
        """
        DESCRIPTION: Navigate to the Fustal event details page from Preconditions
        EXPECTED: It should navigated to Fustal EDP
        """
        pass

    def test_002_verify_the_display_of_penalty_kick_when_a_team_is_awarded_with_penalty_kick(self):
        """
        DESCRIPTION: Verify the display of Penalty kick when a team is awarded with penalty kick
        EXPECTED: The visualization screen should be displayed with the following :
        EXPECTED: Team & Player Name
        EXPECTED: Silk
        EXPECTED: "Penalty" hardcode text
        EXPECTED: Futsal ball Position and Court background color should be  blue
        """
        pass
