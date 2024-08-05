import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.betslip
@vtest
class Test_C647968_Re_establishing_connection_and_receiving_updates_after_inactivity_period(Common):
    """
    TR_ID: C647968
    NAME: Re-establishing connection and receiving updates after inactivity period
    DESCRIPTION: This test case verifies re-establishing connection to LiveServe microservice and receiving LiveServe updates when user brings a browser/app from the background or after a period of sleep in order to receive the latest data of selections in BetSlip
    PRECONDITIONS: * There are added sport and races selection to BetSlip
    PRECONDITIONS: * Browser console is opened
    """
    keep_browser_open = True

    def test_001_lock_device_for_as_much_time_so_it_goes_to_sleep_mode_and_web_socket_connection_to_liveserve_microservice_is_lost(self):
        """
        DESCRIPTION: Lock device for as much time, so it goes to sleep mode and web-socket connection to LiveServe microservice is lost
        EXPECTED: 
        """
        pass

    def test_002_trigger_liveserve_updates_suspension_price_change_etc_for_added_selections(self):
        """
        DESCRIPTION: Trigger LiveServe updates (suspension, price change etc.) for added selections
        EXPECTED: 
        """
        pass

    def test_003_unlock_deviceverify_console(self):
        """
        DESCRIPTION: Unlock device
        DESCRIPTION: Verify console
        EXPECTED: * 'reload components' in console
        EXPECTED: * new active web-socket connection appears
        """
        pass

    def test_004_verify_betslip(self):
        """
        DESCRIPTION: Verify betslip
        EXPECTED: All updates triggered during sleep mode are displayed
        """
        pass

    def test_005_repeat_step_2(self):
        """
        DESCRIPTION: Repeat step #2
        EXPECTED: 
        """
        pass

    def test_006_verify_betslip(self):
        """
        DESCRIPTION: Verify betslip
        EXPECTED: All updates triggered after inactivity period are displayed
        """
        pass

    def test_007_move_app_to_background_for_as_much_time_so_web_socket_connection_to_liveserve_microservice_is_lost(self):
        """
        DESCRIPTION: Move app to background for as much time, so web-socket connection to LiveServe microservice is lost
        EXPECTED: 
        """
        pass

    def test_008_repeat_step_2(self):
        """
        DESCRIPTION: Repeat step #2
        EXPECTED: 
        """
        pass

    def test_009_verify_betslip(self):
        """
        DESCRIPTION: Verify betslip
        EXPECTED: All updates triggered during app being in background are displayed
        """
        pass

    def test_010_move_app_to_foregroundverify_console(self):
        """
        DESCRIPTION: Move app to foreground
        DESCRIPTION: Verify console
        EXPECTED: * 'reload components' in console
        EXPECTED: * new active web-socket connection appears
        """
        pass

    def test_011_repeat_step_2(self):
        """
        DESCRIPTION: Repeat step #2
        EXPECTED: 
        """
        pass

    def test_012_verify_betslip(self):
        """
        DESCRIPTION: Verify betslip
        EXPECTED: All updates triggered during app being in foreground are displayed
        """
        pass

    def test_013_make_device_lose_internet_connection_for_as_much_time_so_web_socket_connection_to_liveserve_microservice_is_lost(self):
        """
        DESCRIPTION: Make device lose internet connection for as much time, so web-socket connection to LiveServe microservice is lost
        EXPECTED: 
        """
        pass

    def test_014_repeat_step_2(self):
        """
        DESCRIPTION: Repeat step #2
        EXPECTED: 
        """
        pass

    def test_015_restore_internet_connectionverify_console(self):
        """
        DESCRIPTION: Restore internet connection
        DESCRIPTION: Verify console
        EXPECTED: * 'reload components' in console
        EXPECTED: * new active web-socket connection appears
        """
        pass

    def test_016_verify_betslip(self):
        """
        DESCRIPTION: Verify betslip
        EXPECTED: All updates triggered during internet connection being lost are displayed
        """
        pass

    def test_017_repeat_step_2(self):
        """
        DESCRIPTION: Repeat step #2
        EXPECTED: 
        """
        pass

    def test_018_verify_betslip(self):
        """
        DESCRIPTION: Verify betslip
        EXPECTED: All updates triggered after restored internet connection are displayed
        """
        pass
