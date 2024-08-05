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
class Test_C59551320_Verify_Betradar_Inplay_event_Corner_Kick(Common):
    """
    TR_ID: C59551320
    NAME: Verify Betradar Inplay event: Corner Kick
    DESCRIPTION: This test case verifies that when there is an incident of Corner Kick in the match Visualization screen displays the  "Corner Kick" text, silk, Player name in the middle and also the Player & Futsal ball position
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
        EXPECTED: It should navigated to Fustal EDP.
        """
        pass

    def test_002_verify_display_of_futsal_inplay_incident_when_team_is_awarded_with_corner_kick(self):
        """
        DESCRIPTION: Verify display of futsal Inplay incident when team is awarded with corner kick
        EXPECTED: The visualization screen should be displayed with the following details:
        EXPECTED: Team & Player Name
        EXPECTED: Silk
        EXPECTED: "Corner kick" hardcode text
        EXPECTED: Futsal ball Position and Court background color should be  blue
        """
        pass
