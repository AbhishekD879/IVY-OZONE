import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.bet_history_open_bets
@vtest
class Test_C60036253_Bet_tracking_Stats_Tracking_for_BYB_5_a_side_error_handling(Common):
    """
    TR_ID: C60036253
    NAME: Bet tracking/Stats Tracking for BYB/5-a-side (error handling)
    DESCRIPTION: This test case verifies 'i' icon displaying and behavior when Opta info can not be displayed for BYB/5-a-side selection
    PRECONDITIONS: * Create a Football event in OpenBet (TI)
    PRECONDITIONS: * Request Banach side to map data including Player Bets markets
    PRECONDITIONS: * Check that Banach data is retrieved (‘events’ request to Banach should return event under test on Football EDP)
    PRECONDITIONS: * Set up Opta Statistic to the created event according to instruction https://confluence.egalacoral.com/display/SDM/Common+match+runner
    PRECONDITIONS: * Place a Build Your Bet/5-a-side bets
    PRECONDITIONS: * Make sure that Opta info can not be displayed for placed selections e.g. data mismatch, no data on Opta
    PRECONDITIONS: * In OpenBet (TI) event should be Live (Is OFF = Yes)
    PRECONDITIONS: * Load app and log in
    PRECONDITIONS: * To check Opta live updates subscription open Dev Tools -> Network tab -> WS -> select request to Live Serve MS
    PRECONDITIONS: * Endpoints to Live Serve MS:
    PRECONDITIONS: wss://liveserve-publisher-dev1.coralsports.dev.cloud.ladbrokescoral.com/websocket/?EIO=3&transport=websocket - dev1
    """
    keep_browser_open = True

    def test_001_go_to_open_bets_tabpage(self):
        """
        DESCRIPTION: Go to 'Open bets' tab/page
        EXPECTED: * Build Your Bet bet is present on 'Open bets' tab/page with selections with Binary and Range templates
        EXPECTED: * WS connection with Live Serve MS is created
        EXPECTED: 42["scoreboard","eventID"] request is sent to subscribe for Opta updates
        EXPECTED: * Initial data structure response is received
        """
        pass

    def test_002_go_build_your_bet_bet_where_opta_info_can_not_be_displayed_for_selection(self):
        """
        DESCRIPTION: Go Build Your Bet bet where Opta info can not be displayed for selection
        EXPECTED: * Pre-match view is displayed for selection
        EXPECTED: * 'i' icon is displayed next to the selection
        """
        pass

    def test_003_tapclick_on_the_i_icon(self):
        """
        DESCRIPTION: Tap/click on the 'i' icon
        EXPECTED: Tooltip is displayed with the next text:
        EXPECTED: 'Stats Unavailable For This Selection'
        EXPECTED: ![](index.php?/attachments/get/121534902)
        """
        pass

    def test_004_tapclick_away_tooltip(self):
        """
        DESCRIPTION: Tap/click away tooltip
        EXPECTED: * Tooltip is no more shown
        """
        pass
