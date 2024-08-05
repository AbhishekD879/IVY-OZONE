import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.cash_out
@vtest
class Test_C647971_Re_establishing_connection_and_receiving_updates_after_inactivity_period_Cashout_tab(Common):
    """
    TR_ID: C647971
    NAME: Re-establishing connection and receiving updates after inactivity period (Cashout tab)
    DESCRIPTION: This test case verifies re-establishing connection to LiveServe microservice and receiving LiveServe updates when user brings a browser/app from the background or after a period of sleep in order to receive the latest data of selections on 'Cash Out' tab
    PRECONDITIONS: * User has single and multiple placed bets on sport and races events with available cash out
    PRECONDITIONS: * Browser console is opened
    PRECONDITIONS: **From release XXX.XX (according to BMA-50940/BMA-50937/BMA-50936):**
    PRECONDITIONS: - WebSocket connection to Cashout MS is created when user lands on myBets/Cashout page
    PRECONDITIONS: - No requests to BPP getBetDetails and getBetDetail should be performed on cashout page
    """
    keep_browser_open = True

    def test_001_navigate_to_cash_out_tab_on_my_bets_pagebet_slip_widget(self):
        """
        DESCRIPTION: Navigate to 'Cash out' tab on 'My Bets' page/'Bet Slip' widget
        EXPECTED: 
        """
        pass

    def test_002_lock_device_for_as_much_time_so_it_goes_to_sleep_mode_and_websocket_connection_to_liveserve_microservice_is_lost(self):
        """
        DESCRIPTION: Lock device for as much time, so it goes to sleep mode and websocket connection to LiveServe microservice is lost
        EXPECTED: 
        """
        pass

    def test_003_trigger_liveserve_updates_suspension_price_change_etc_for_bets_in_cash_out(self):
        """
        DESCRIPTION: Trigger LiveServe updates (suspension, price change etc.) for bets in Cash Out
        EXPECTED: 
        """
        pass

    def test_004_unlock_deviceverify_console(self):
        """
        DESCRIPTION: Unlock device
        DESCRIPTION: Verify console
        EXPECTED: * 'reload components' in console
        EXPECTED: * new active websocket connection appears
        EXPECTED: * getbetdetails request is sent
        EXPECTED: **From release XXX.XX:**
        EXPECTED: * 'reload components' in console
        EXPECTED: * cashoutUpdate are received in WebSocket connection to Cash Out MS
        EXPECTED: * new WebSocket connection to Cash Out MS is set up
        """
        pass

    def test_005_verify_cash_out_tab(self):
        """
        DESCRIPTION: Verify 'Cash out' tab
        EXPECTED: Content of tab is reloaded and all updates triggered during sleep mode are displayed
        """
        pass

    def test_006_repeat_step_3(self):
        """
        DESCRIPTION: Repeat step #3
        EXPECTED: 
        """
        pass

    def test_007_verify_cash_out_tab(self):
        """
        DESCRIPTION: Verify 'Cash out' tab
        EXPECTED: All updates triggered after inactivity period are displayed
        """
        pass

    def test_008_move_app_to_background_for_as_much_time_so_websocket_connection_to_liveserve_microservice_is_lost(self):
        """
        DESCRIPTION: Move app to background for as much time, so websocket connection to LiveServe microservice is lost
        EXPECTED: 
        """
        pass

    def test_009_repeat_step_3(self):
        """
        DESCRIPTION: Repeat step #3
        EXPECTED: 
        """
        pass

    def test_010_verify_cash_out_tab(self):
        """
        DESCRIPTION: Verify 'Cash out' tab
        EXPECTED: All updates triggered during app being in background are displayed
        """
        pass

    def test_011_move_app_to_foregroundverify_console(self):
        """
        DESCRIPTION: Move app to foreground
        DESCRIPTION: Verify console
        EXPECTED: * 'reload components' in console
        EXPECTED: * new active websocket connection appears
        EXPECTED: * getbetdetails request is sent
        EXPECTED: **From release XXX.XX:**
        EXPECTED: * 'reload components' in console
        EXPECTED: * cashoutUpdate are received in WebSocket connection to Cash Out MS
        EXPECTED: * new WebSocket connection to Cash Out MS is set up
        """
        pass

    def test_012_repeat_step_3(self):
        """
        DESCRIPTION: Repeat step #3
        EXPECTED: 
        """
        pass

    def test_013_verify_cash_out_tab(self):
        """
        DESCRIPTION: Verify 'Cash out' tab
        EXPECTED: Content of tab is reloaded and all updates triggered during app being in foreground are displayed
        """
        pass

    def test_014_make_device_lose_internet_connection_for_as_much_time_so_websocket_connection_to_liveserve_microservice_is_lost(self):
        """
        DESCRIPTION: Make device lose internet connection for as much time, so websocket connection to LiveServe microservice is lost
        EXPECTED: 
        """
        pass

    def test_015_repeat_step_3(self):
        """
        DESCRIPTION: Repeat step #3
        EXPECTED: 
        """
        pass

    def test_016_restore_internet_connectionverify_console(self):
        """
        DESCRIPTION: Restore internet connection
        DESCRIPTION: Verify console
        EXPECTED: * 'reload components' in console
        EXPECTED: * new active websocket connection appears
        EXPECTED: * getbetdetails request is sent
        EXPECTED: **From release XXX.XX:**
        EXPECTED: * 'reload components' in console
        EXPECTED: * cashoutUpdate are received in WebSocket connection to Cash Out MS
        EXPECTED: * new WebSocket connection to Cash Out MS is set up
        """
        pass

    def test_017_verify_cash_out_tab(self):
        """
        DESCRIPTION: Verify 'Cash out' tab
        EXPECTED: Content of tab is reloaded and all updates triggered during internet connection being lost are displayed
        """
        pass

    def test_018_repeat_step_3(self):
        """
        DESCRIPTION: Repeat step #3
        EXPECTED: 
        """
        pass

    def test_019_verify_cash_out_tab(self):
        """
        DESCRIPTION: Verify 'Cash out' tab
        EXPECTED: All updates triggered after restored internet connection are displayed
        """
        pass
