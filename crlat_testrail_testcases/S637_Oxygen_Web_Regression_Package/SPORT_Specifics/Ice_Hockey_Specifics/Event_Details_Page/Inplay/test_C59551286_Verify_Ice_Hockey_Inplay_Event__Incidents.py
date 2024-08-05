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
class Test_C59551286_Verify_Ice_Hockey_Inplay_Event__Incidents(Common):
    """
    TR_ID: C59551286
    NAME: Verify Ice Hockey Inplay Event - Incidents
    DESCRIPTION: This test case verifies incidents for an inplay event with betradar visualization
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

    def test_002_click_on_statistics_tab(self):
        """
        DESCRIPTION: Click on 'Statistics' tab
        EXPECTED: Statistics tab should be opened
        """
        pass

    def test_003_verify_statistics_values_displaying(self):
        """
        DESCRIPTION: Verify statistics values displaying
        EXPECTED: Each of the stats type have values (numbers) on the player corresponding side
        EXPECTED: Each of the stats has a incident name with a graph representing player statistics
        """
        pass

    def test_004_verify_names_at_the_top_of_each_statistics(self):
        """
        DESCRIPTION: Verify names at the top of each statistics
        EXPECTED: Below names are displayed for overall match and also for each set separately
        EXPECTED: + TOTAL POINTS WON
        EXPECTED: + SERVER and RECEIVER POINTS
        EXPECTED: + MAX POINTS IN A ROW
        EXPECTED: + SERVICE ERRORS
        EXPECTED: + TIMEOUTS
        EXPECTED: + COMEBACK TO WIN
        """
        pass

    def test_005_verify_total_points_won_values(self):
        """
        DESCRIPTION: Verify TOTAL POINTS WON values
        EXPECTED: When a player WON a point then corresponding player TOTAL POINTS WON Stats value is increased by one in overall Match points and also in current SET playing
        """
        pass

    def test_006_verify_server_and_receiver_points_values(self):
        """
        DESCRIPTION: Verify SERVER and RECEIVER POINTS values
        EXPECTED: SERVER and RECEIVER POINTS stats value will increase when a corresponding incident happens
        """
        pass

    def test_007_verify_max_points_in_a_row_values(self):
        """
        DESCRIPTION: Verify MAX POINTS IN A ROW values
        EXPECTED: MAX POINTS IN A ROW stats values will be increased when corresponding player scores points in a row
        """
        pass

    def test_008_verify_service_errors_values(self):
        """
        DESCRIPTION: Verify SERVICE ERRORS values
        EXPECTED: SERVICE ERRORS stats value will be increased when a corresponding player does following:
        EXPECTED: + Player serves but missed to bounce first step in his court
        EXPECTED: + Player has served out of turn
        EXPECTED: + Player has served to the wrong service court
        EXPECTED: + Player standing on the wrong service court while serving and it has been delivered
        """
        pass

    def test_009_verify_timeouts_values(self):
        """
        DESCRIPTION: Verify TIMEOUTS values
        EXPECTED: TIMEOUTS stats value will be increased when a corresponding player request for timeout
        """
        pass

    def test_010_verify_comeback_to_win_values(self):
        """
        DESCRIPTION: Verify COMEBACK TO WIN values
        EXPECTED: COMEBACK TO WIN stats value will be increased when a corresponding player makes a comeback
        """
        pass
