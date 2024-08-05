import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.sports
@vtest
class Test_C336790_Websocket_connection_re_establishment(Common):
    """
    TR_ID: C336790
    NAME: Websocket connection re-establishment
    DESCRIPTION: This test case verifies tennis websocket connection re-establishment after losing and restoring the connection to the Internet or coming back from sleep mode.
    PRECONDITIONS: * Tennis Visualization is mapped to live event (can be checked in [Mapper Tool][1])
    PRECONDITIONS: [1]: https://coral-vis-rtc-tst2.symphony-solutions.eu/#/sports/tennis/provider/img/tournaments/all/events?_k=smo0sj
    """
    keep_browser_open = True

    def test_001_navigate_to_event_details_page_of_event_from_preconditions(self):
        """
        DESCRIPTION: Navigate to Event Details page of event from preconditions
        EXPECTED: Tennis Visualization iframe is displayed
        """
        pass

    def test_002_lock_device_for_few_minutes_so_it_goes_to_sleep_mode(self):
        """
        DESCRIPTION: Lock device for few minutes, so it goes to sleep mode
        EXPECTED: 
        """
        pass

    def test_003_unlock_device(self):
        """
        DESCRIPTION: Unlock device
        EXPECTED: 
        """
        pass

    def test_004_verify_tennis_visualization_behaviour(self):
        """
        DESCRIPTION: Verify tennis visualization behaviour
        EXPECTED: * Last up-do-date incident (received in websocket) is displayed within iframe
        EXPECTED: * Scores and sets are updated correctly
        EXPECTED: * New incidents are received in websocket and shown on front end
        EXPECTED: * Statistic on second slide is updated correctly
        """
        pass

    def test_005_move_app_to_background_for_few_minutes(self):
        """
        DESCRIPTION: Move app to background for few minutes
        EXPECTED: 
        """
        pass

    def test_006_move_app_to_foreground(self):
        """
        DESCRIPTION: Move app to foreground
        EXPECTED: 
        """
        pass

    def test_007_repeat_step_4(self):
        """
        DESCRIPTION: Repeat step #4
        EXPECTED: 
        """
        pass

    def test_008_make_device_lose_internet_connection_and_wait_few_minutes(self):
        """
        DESCRIPTION: Make device lose internet connection and wait few minutes
        EXPECTED: Pop up about loosing internet appears
        """
        pass

    def test_009_close_pop_up(self):
        """
        DESCRIPTION: Close pop up
        EXPECTED: 
        """
        pass

    def test_010_restore_internet_connection_it_may_take_some_time(self):
        """
        DESCRIPTION: Restore internet connection (it may take some time)
        EXPECTED: 
        """
        pass

    def test_011_repeat_step_4(self):
        """
        DESCRIPTION: Repeat step #4
        EXPECTED: 
        """
        pass
