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
class Test_C59551284_Verify_Ice_Hockey_Inplay_event_End_of_the_Period(Common):
    """
    TR_ID: C59551284
    NAME: Verify Ice Hockey Inplay event: End of the Period
    DESCRIPTION: This test case verifies END of the PERIOD of an inplay event with betradar visualization
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

    def test_002_wait_for_the_end_of_period(self):
        """
        DESCRIPTION: Wait for the end of PERIOD
        EXPECTED: + 'SET WON' message should be shown below the corresponding player name
        EXPECTED: + Number of sets in score line is equal with number of played sets
        EXPECTED: + Score line is updated according to set results
        EXPECTED: + Score box is displayed in table tennis court widget with player names and Number of sets won by each player
        EXPECTED: + After 2 seconds slides are displayed until next SET starts
        EXPECTED: 1st slide - **Basic Event Information** - League, Date and
        EXPECTED: Time, Player names with score and Match status as Break
        EXPECTED: 2nd and 3rd slide - **Match Statistics**
        EXPECTED: 4th slide - **Head to Head statistics**
        EXPECTED: 5th slide - **WIN Probability**
        """
        pass

    def test_003_verify_starting_of_next_period(self):
        """
        DESCRIPTION: Verify Starting of Next PERIOD
        EXPECTED: + Next SET name should be displayed in square box with a timer icon on table tennis widget
        EXPECTED: + After 2 seconds SCORE Box should be displayed and the ball rally animation starts
        EXPECTED: + Current SET name is updated across the widget
        """
        pass
