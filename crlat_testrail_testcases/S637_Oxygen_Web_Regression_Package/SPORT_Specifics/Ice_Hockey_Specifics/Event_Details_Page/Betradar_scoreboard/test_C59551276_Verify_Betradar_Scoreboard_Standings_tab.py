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
class Test_C59551276_Verify_Betradar_Scoreboard_Standings_tab(Common):
    """
    TR_ID: C59551276
    NAME: Verify Betradar Scoreboard- Standings tab
    DESCRIPTION: This test case verifies standings tab of an event with betradar visualization
    PRECONDITIONS: Make sure you have Ice Hockey Inplay event which is subscribed to Betradar Scoreboards
    PRECONDITIONS: Navigate to Inplay-> Ice Hockey -> Tap on event (which is subscribed to betradar)
    PRECONDITIONS: How to check event is mapped to betradar or not?
    PRECONDITIONS: inspect elements click on inplay event and while loading EDP check for api-key network call. if we get 200 response then event has betradar and if we get 404 this event should show fallback
    PRECONDITIONS: Confluence link:
    PRECONDITIONS: https://confluence.egalacoral.com/pages/viewpage.action?pageId=139380661
    """
    keep_browser_open = True

    def test_001_navigate_to_event_details_page_of_inplay_event_as_per_the_pre_conditions(self):
        """
        DESCRIPTION: Navigate to Event Details Page of Inplay event as per the pre-conditions
        EXPECTED: Event Details Page should be opened with match visualization and scoreboards
        """
        pass

    def test_002_click_on_standings_tab(self):
        """
        DESCRIPTION: Click on 'Standings' tab
        EXPECTED: Standings tab should be opened
        """
        pass

    def test_003_verify_display_of_standings_tab_when_data_is_not_available(self):
        """
        DESCRIPTION: Verify display of standings tab when data is not available
        EXPECTED: 'No Statistics available' message should be displayed with a dummy graph
        """
        pass

    def test_004_verify_display_of_standings_tab_when_data_is_available(self):
        """
        DESCRIPTION: Verify display of standings tab when data is available
        EXPECTED: 
        """
        pass
