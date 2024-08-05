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
class Test_C59551273_Verify_Betradar_Scoreboard_list_of_tabs(Common):
    """
    TR_ID: C59551273
    NAME: Verify Betradar Scoreboard- list of tabs
    DESCRIPTION: This test case verifies list of tabs present in betradar visualization
    PRECONDITIONS: Make sure the Ice Hockey Inplay event which is subscribed to Betradar Scoreboards
    PRECONDITIONS: Navigate to Inplay-> Ice Hockey -> Tap on event (which is subscribed to betradar)
    PRECONDITIONS: How to check event is mapped to betradar or not?
    PRECONDITIONS: inspect elements click on inplay event and while loading EDP check for api-key network call. if we get 200 response then event has betradar and if we get 404 this event should show fallback
    PRECONDITIONS: Confluence link:
    PRECONDITIONS: https://confluence.egalacoral.com/pages/viewpage.action?pageId=139380661
    """
    keep_browser_open = True

    def test_001_navigate_to_event_details_page_of_inplay_ice_hockey_event_as_per_the_pre_conditions(self):
        """
        DESCRIPTION: Navigate to Event Details Page of Inplay Ice Hockey event as per the pre-conditions
        EXPECTED: Event Details Page should be opened with match visualization and scoreboards
        """
        pass

    def test_002_verify_list_of_available_tabs_in_betradar(self):
        """
        DESCRIPTION: Verify list of available tabs in betradar
        EXPECTED: a. Pitch
        EXPECTED: b. Statistics
        EXPECTED: c. Head to Head
        EXPECTED: d. Standings
        EXPECTED: e. Timelines
        """
        pass
