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
class Test_C59551324_Verify_that_when_Betradar_Scoreboard_Visualisation_in_EDP_of_In_Play_event(Common):
    """
    TR_ID: C59551324
    NAME: Verify that when Betradar Scoreboard Visualisation in EDP of In-Play event
    DESCRIPTION: This test case verifies In Play Fustal event that is subscribed to Betradar Scoreboard.
    PRECONDITIONS: 1: Navigate to Sports Menu(Fustal)/From A-Z all Sports->Fustal
    PRECONDITIONS: 2: Event should be In-Play.
    PRECONDITIONS: 3:Betradar scoreboard configuration in CMS is enabled.
    PRECONDITIONS: TBD?
    PRECONDITIONS: CMS > System Configuration > Structure > Betradar Scoreboard
    PRECONDITIONS: URL:
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

    def test_002_swipe_through_bet_radar_scoreboard__visualisation_screens(self):
        """
        DESCRIPTION: Swipe through Bet radar Scoreboard & Visualisation screens
        EXPECTED: User is able to navigate between Bet radar Scoreboard screens
        """
        pass
