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
class Test_C59551285_Verify_Ice_Hockey_Inplay_event_End_of_the_Match(Common):
    """
    TR_ID: C59551285
    NAME: Verify Ice Hockey Inplay event: End of the Match
    DESCRIPTION: This test case verifies END of the MATCH of an inplay event with betradar visualization
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

    def test_002_wait_for_the_end_of_match(self):
        """
        DESCRIPTION: Wait for the end of match
        EXPECTED: 'MATCH WON' message should be shown below the corresponding player name
        EXPECTED: Score is displayed in top with player names, Number of sets won by each player and Match Status as 'Ended'
        """
        pass

    def test_003_verify_slides_after_end_of_match(self):
        """
        DESCRIPTION: Verify slides after end of match
        EXPECTED: 1st slide - Basic Event Information - League, Date and
        EXPECTED: Time, Player names with score and Match status as Ended
        EXPECTED: 2nd and 3rd slide - Match Statistics
        EXPECTED: 4th slide - Head to Head statistics
        """
        pass
