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
class Test_C336789_Websocket_connection_re_establishment__Football_Visualization(Common):
    """
    TR_ID: C336789
    NAME: Websocket connection re-establishment - Football Visualization
    DESCRIPTION: This test case verifies football websocket connection re-establishment after losing and restoring the connection to the Internet or coming back from sleep mode.
    PRECONDITIONS: Football Visualization is mapped to event (can be checked in [Mapper Tool][1])
    PRECONDITIONS: [1]: https://coral-vis-rtc-tst2.symphony-solutions.eu/#/sports/football/provider/openbet/tournaments/all/events?_k=qasfl6
    """
    keep_browser_open = True

    def test_001_navigate_to_event_details_page_of_event_from_preconditions(self):
        """
        DESCRIPTION: Navigate to Event Details page of event from preconditions
        EXPECTED: Football Visualization iframe is displayed
        """
        pass

    def test_002_lock_device_for_few_minutes_so_it_goes_to_sleep_mode(self):
        """
        DESCRIPTION: Lock device for few minutes, so it goes to sleep mode
        EXPECTED: 
        """
        pass

    def test_003_unlock_deviceverify_console(self):
        """
        DESCRIPTION: Unlock device
        DESCRIPTION: Verify console
        EXPECTED: 'reload components' in console
        """
        pass

    def test_004_verify__football_visualization_behaviour(self):
        """
        DESCRIPTION: Verify  football visualization behaviour
        EXPECTED: * Last up-do-date incident (received in websocket) is displayed within iframe
        EXPECTED: * Scores are up to date
        EXPECTED: * Statistics are up to date
        """
        pass

    def test_005_move_app_to_background_for_few_minutes(self):
        """
        DESCRIPTION: Move app to background for few minutes
        EXPECTED: 
        """
        pass

    def test_006_move_app_to_foregroundverify_console(self):
        """
        DESCRIPTION: Move app to foreground
        DESCRIPTION: Verify console
        EXPECTED: 'reload components' in console
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

    def test_010_restore_internet_connection_it_may_take_some_timeverify_console(self):
        """
        DESCRIPTION: Restore internet connection (it may take some time)
        DESCRIPTION: Verify console
        EXPECTED: 'reload components' in console
        """
        pass

    def test_011_repeat_step_4(self):
        """
        DESCRIPTION: Repeat step #4
        EXPECTED: 
        """
        pass
