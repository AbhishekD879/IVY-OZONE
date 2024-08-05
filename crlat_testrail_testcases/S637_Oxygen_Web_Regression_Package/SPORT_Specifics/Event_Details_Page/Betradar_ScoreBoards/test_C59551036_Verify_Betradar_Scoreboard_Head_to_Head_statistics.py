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
class Test_C59551036_Verify_Betradar_Scoreboard_Head_to_Head_statistics(Common):
    """
    TR_ID: C59551036
    NAME: Verify Betradar Scoreboard-Head to Head statistics
    DESCRIPTION: This test case verifies head to head statistics for an event with betradar visualization
    PRECONDITIONS: Make sure you have Table Tennis Inplay event which is subscribed to Betradar Scoreboards
    PRECONDITIONS: Navigate to Inplay-> Table Tennis -> Tap on event (which is subscribed to betradar)
    PRECONDITIONS: How to check whether event is mapped to betradar or not?
    PRECONDITIONS: inspect elements click on inplay event and while loading EDP check for api-key network call. if we get 200 response then event has betradar scoreboard and if we get 404 this event should show fallback
    PRECONDITIONS: Confluence link
    PRECONDITIONS: https://confluence.egalacoral.com/pages/viewpage.action?pageId=139380661
    """
    keep_browser_open = True

    def test_001_navigate_to_event_details_page_of_inplay_event_as_per_the_pre_conditions(self):
        """
        DESCRIPTION: Navigate to Event Details Page of Inplay event as per the pre-conditions
        EXPECTED: Event Details Page should be opened with match visualization and scoreboards.
        """
        pass

    def test_002_click_on_head_to_head__tab(self):
        """
        DESCRIPTION: Click on 'Head to Head ' tab
        EXPECTED: HEAD TO HEAD tab should be opened
        """
        pass

    def test_003_verify_the_view_of_head_to_head_results(self):
        """
        DESCRIPTION: Verify the view of Head to Head results
        EXPECTED: + Last 5 results (W Or L) of Head to Head meetings are displayed separated by horizontal line(-) on corresponding sides of both players
        EXPECTED: + Bar graphs are displayed with percentage indicating player form in last 5 matches
        """
        pass

    def test_004_verify_the_view_of_bar_graphs(self):
        """
        DESCRIPTION: Verify the view of bar graphs
        EXPECTED: + Emphasis of bar is shown high for player having more number of wins
        EXPECTED: + If both players have won same number of matches then the emphasis of bar should be equal on both sides
        """
        pass
