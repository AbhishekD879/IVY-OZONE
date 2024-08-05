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
class Test_C59551350_Verify_Betradar_Inplay_event_Suspension(Common):
    """
    TR_ID: C59551350
    NAME: Verify Betradar Inplay event: Suspension
    DESCRIPTION: This test case verifies that when there is an incident of Free throw in the match Visualization screen displays the  "Suspension" text, silk, Player name in the middle and also the Player & Handball position.
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
        EXPECTED: It should navigated to Handball EDP
        """
        pass

    def test_002_verify_the_display_of_free_throw_visualization_screen_when_a_player_is_suspension(self):
        """
        DESCRIPTION: Verify the display of Free throw visualization screen when a player is Suspension
        EXPECTED: The visualization screen should be displayed with the following :
        EXPECTED: Team & Player Name
        EXPECTED: Silk
        EXPECTED: "Suspension" hardcode text
        EXPECTED: Handball ball Position and Court background color should be  blue
        """
        pass
