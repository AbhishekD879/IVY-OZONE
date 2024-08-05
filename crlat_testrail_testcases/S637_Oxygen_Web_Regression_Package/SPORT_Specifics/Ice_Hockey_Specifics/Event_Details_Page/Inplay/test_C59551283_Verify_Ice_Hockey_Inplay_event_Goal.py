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
class Test_C59551283_Verify_Ice_Hockey_Inplay_event_Goal(Common):
    """
    TR_ID: C59551283
    NAME: Verify Ice Hockey Inplay event: Goal
    DESCRIPTION: This test case verifies display of DEUCE of an inplay event with betradar visualization
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

    def test_002_verify_display_of_goal(self):
        """
        DESCRIPTION: Verify display of Goal
        EXPECTED: Goal message should be shown when both the players score 10 points i.e, tie
        EXPECTED: *this tie must be broken by someone scoring two points in a row
        """
        pass
