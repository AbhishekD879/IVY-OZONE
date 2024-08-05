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
class Test_C43873657_Cashout_MS_price_updates_aggregation(Common):
    """
    TR_ID: C43873657
    NAME: Cashout MS  price updates aggregation
    DESCRIPTION: TC verifies that if in N seconds microservice received selection updates for the same bet id, they are grouped and processed in normal flow (only one message is received from Cashout MS on Frontend).
    DESCRIPTION: **From release XXX.XX (according to BMA-50940/BMA-50937/BMA-50936):**
    DESCRIPTION: - WebSocket connection to Cashout MS is created when user lands on myBets/Cashout page
    PRECONDITIONS: 1. Multiple bet is placed with cashout available.
    PRECONDITIONS: 2. Two events from multiple bet are opened in separate TI windows.
    PRECONDITIONS: 3. My bets page is opened in app.
    PRECONDITIONS: ------------------------------------------------------------------------------------
    PRECONDITIONS: Following property sets the timeframe when messages should be grouped, '1s' means that if two updates are coming within the interval of 1s - they should be grouped and sent to Frontend as a single update (it is required to look in the code to find out configuration set)
    PRECONDITIONS: >    cashoutOffer.buffering.windowTime=1s
    PRECONDITIONS: To trigger simultaneous 'save' button click in TI on market page for a few selection (for Ladbrokes), run following in both TI windows (with desired time of trigger instead of 1995-12-17T03:24:00):
    PRECONDITIONS: >    var triggerDelay = new Date('1995-12-17T03:24:00') - new Date();
    PRECONDITIONS: >    setTimeout(() => document.querySelector('#submit_button>div.middle').click(), triggerDelay);
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+trigger+simultaneous+%27save%27+button+click+in+TI+on+market+page+for+a+few+selection
    """
    keep_browser_open = True

    def test_001_in_app_open_network_tab_in_devtools_search_for_cashoutfrom_release_xxxxxin_app_open_open_dev_tools___network_tab___ws_filter_search_for_cashout(self):
        """
        DESCRIPTION: In App: open Network tab in devtools, search for 'cashout'
        DESCRIPTION: **From release XXX.XX:**
        DESCRIPTION: In App: open Open Dev Tools -> Network tab -> WS filter, search for 'cashout'
        EXPECTED: Cashout messages are opened
        EXPECTED: Ex. url: https://cashout-dev0.ladbrokesoxygen.dev.cloud.ladbrokescoral.com/bet-details?token=6168b7a60895f4b66a3aac840b44a7d2fbaef9352c9ad923fe1cc35aecd17601
        EXPECTED: **From release XXX.XX:**
        EXPECTED: WebSocket connection to Cashout MS is created.
        EXPECTED: Ex. url: wss://cashout-dev0.coralsports.dev.cloud.ladbrokescoral.com:8443/socket.io/?token=b5ad14dd39ab488ad2e89e24be6d2a11e5637889349fb8ea8e31819d39b62a23&EIO=3&transport=websocket
        """
        pass

    def test_002_in_ti_trigger_price_update_for_both_selections_simultaneously(self):
        """
        DESCRIPTION: In TI: trigger price update for both selections simultaneously
        EXPECTED: 
        """
        pass

    def test_003_in_app_check_update_received_from_cashout_ms(self):
        """
        DESCRIPTION: In App: check update received from Cashout MS
        EXPECTED: Only one update is received.
        EXPECTED: Ex: cashoutUpdate {"cashoutData":{"betId":"69247","cashoutValue":"0.6"}}
        """
        pass

    def test_004_in_app_check_that_new_cashout_value_is_displayed_in_my_bets(self):
        """
        DESCRIPTION: In App: check that new cashout value is displayed in My Bets
        EXPECTED: 
        """
        pass
