import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.bet_history_open_bets
@vtest
class Test_C59997791_Verify_Bet_Tracker_info_for_Pre_Match_event(Common):
    """
    TR_ID: C59997791
    NAME: Verify Bet Tracker info for Pre Match event
    DESCRIPTION: This test case verifies Bet Tracker info for Pre Match event
    PRECONDITIONS: * Make sure that Bet Tracking feature is enabled in CMS: System-configuration -> Structure -> BetTracking config -> enabled = true
    PRECONDITIONS: * Create a Football event in OpenBet (T.I.) and make sure that event is not started (In TI set 'Іs Off' = no)
    PRECONDITIONS: * Request Banach side to map data including Player Bets markets
    PRECONDITIONS: * Check that Banach data is retrieved (‘events’ request to Banach should return event under test on Football EDP)
    PRECONDITIONS: * Place a Build Your Bet/5-a-side bets
    PRECONDITIONS: * Set up Opta Statistic to the created event to be started in the future (Pre Play view) according to instruction https://confluence.egalacoral.com/display/SDM/Common+match+runner
    PRECONDITIONS: * Load app and log in
    PRECONDITIONS: * To check Opta live updates subscription open Dev Tools -> Network tab -> WS -> select request to Live Serv MS
    PRECONDITIONS: * Endpoints to Live Serv MS:
    PRECONDITIONS: - wss://liveserve-publisher-dev1.coralsports.dev.cloud.ladbrokescoral.com/websocket/?EIO=3&transport=websocket - dev1
    """
    keep_browser_open = True

    def test_001_go_to_open_bets_pagetab(self):
        """
        DESCRIPTION: Go to Open Bets page/tab
        EXPECTED: * Open Bets page/tab is opened
        EXPECTED: * WS connection to Live Serv MS is created
        EXPECTED: * Event is NOT subscribed for Opta updates
        EXPECTED: * No subscription request 42["scoreboard","eventID"] is sent,
        EXPECTED: where 'eventID' - id of created event in OB
        """
        pass

    def test_002_go_to_build_your_bet_and_check_its_displaying(self):
        """
        DESCRIPTION: Go to Build Your Bet and check its displaying
        EXPECTED: * Title is BUILD YOUR BET (for Coral) / BET BUILDER (for Ladbrokes)
        EXPECTED: * Grey bar with pips connecting selections is shown
        EXPECTED: * Left-hand status indicators for the bet's selections are NOT displayed
        EXPECTED: * Progress bars and stats descriptions for the bet's selections are NOT displayed
        EXPECTED: ![](index.php?/attachments/get/120825954)
        EXPECTED: ![](index.php?/attachments/get/120825955)
        """
        pass

    def test_003_go_to_5_a_side_bet_and_check_its_displaying(self):
        """
        DESCRIPTION: Go to 5-a-side Bet and check its displaying
        EXPECTED: * Title is 5-A-SIDE
        EXPECTED: * Grey bar with pips connecting selections is shown
        EXPECTED: * Left-hand status indicators for the bet's selections are NOT displayed
        EXPECTED: * Progress bars and stats descriptions for the bet's selections are NOT displayed
        """
        pass

    def test_004_go_to_settled_bets_tab_and_repeat_steps_2_3(self):
        """
        DESCRIPTION: Go to 'Settled Bets' tab and repeat steps #2-3
        EXPECTED: 
        """
        pass

    def test_005_go_to_cash_out_tab_and_repeat_steps_2_3_coral_only(self):
        """
        DESCRIPTION: Go to 'Cash Out' tab and repeat steps #2-3 (Coral only)
        EXPECTED: 
        """
        pass

    def test_006_go_to_my_bets_tab_on_edp_and_repeat_steps_2_3_coral_only(self):
        """
        DESCRIPTION: Go to 'My Bets' tab on EDP and repeat steps #2-3 (Coral only)
        EXPECTED: 
        """
        pass
