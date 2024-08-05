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
class Test_C59551349_Verify_Betradar_Inplay_event_yellow_red_cards(Common):
    """
    TR_ID: C59551349
    NAME: Verify Betradar Inplay event: yellow/red cards
    DESCRIPTION: This test case verifies  that when there is an incident of Misconduct in the match Visualization screen displays the Yellow/Red Card given to the Player
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
        EXPECTED: It should be navigated to Handball EDP
        """
        pass

    def test_002_verify_display_of_handball_inplay_incident_when_team_receives_yellowred_cards(self):
        """
        DESCRIPTION: Verify display of Handball Inplay incident when team receives yellow/red cards
        EXPECTED: The visualization screen should be displayed with the following :
        EXPECTED: Team & Player Name
        EXPECTED: Silk
        EXPECTED: Card details like Yellow/Red card
        """
        pass
