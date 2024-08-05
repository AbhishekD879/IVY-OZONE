import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.5_a_side
@vtest
class Test_C59471247_Verify_Bet_Tracker_info_when_event_has_finished(Common):
    """
    TR_ID: C59471247
    NAME: Verify Bet Tracker info when event has finished
    DESCRIPTION: This test case verifies Bet Tracker info when event has finished
    PRECONDITIONS: * Make sure that Bet Tracking feature is enabled in CMS: System-configuration -> Structure -> BetTracking config -> enabled = true
    PRECONDITIONS: * Create a Football event in OpenBet (T.I.)
    PRECONDITIONS: * Request Banach side to map data including Player Bets markets
    PRECONDITIONS: * Check that Banach data is retrieved (‘events’ request to Banach should return event under test on Football EDP)
    PRECONDITIONS: * Place a Build Your Bet/5-a-side bets with selection template = Range and template = Binary
    PRECONDITIONS: * Set up Opta Statistic to the created event according to instruction https://confluence.egalacoral.com/display/SDM/Common+match+runner
    PRECONDITIONS: * Start recorded event (In TI set 'Іs Off' = yes)
    PRECONDITIONS: * Load app and log in
    PRECONDITIONS: * Go to Open Bets page/tab -> event subscription for Opta updates should be made in Live Serv MS: 42["scoreboard","eventID"] and initial response must be received
    PRECONDITIONS: * To check Opta live updates open Dev Tools -> Network tab -> WS -> select request to Live Serv MS
    PRECONDITIONS: * To check OpenBet Outcome Statuses: Dev tools > Network find accountHistory request
    PRECONDITIONS: * Endpoints to Live Serv MS:
    PRECONDITIONS: - wss://liveserve-publisher-dev1.coralsports.dev.cloud.ladbrokescoral.com/websocket/?EIO=3&transport=websocket - dev1
    PRECONDITIONS: **NOTE**
    PRECONDITIONS: Selections with 'template = Binary' means that only 2 options are available. E.g. 'Both Team to score' -> Yes/No.
    PRECONDITIONS: Selections with template = Range' means that multiple-choice prediction is available. E.g. 'Christain Eriksen to Make 55+ Passes'
    """
    keep_browser_open = True

    def test_001_go_to_build_your_bet_bet(self):
        """
        DESCRIPTION: Go to **Build Your Bet** bet
        EXPECTED: 
        """
        pass

    def test_002_settle_event_in_ob_ti_tool_or_wait_until_its_ended(self):
        """
        DESCRIPTION: Settle event in OB TI tool or wait until it's ended
        EXPECTED: * Event should be settled
        EXPECTED: * Bet with settled event disappears from 'Open Bets' tab/page
        """
        pass

    def test_003_go_to_settled_bets_tab(self):
        """
        DESCRIPTION: Go to 'Settled bets' tab
        EXPECTED: * 'Settled bets' tab is opened
        EXPECTED: * Status for Event is received from OpenBet
        EXPECTED: * The very last updated is received
        """
        pass

    def test_004_check_build_your_bet_betdisplaying(self):
        """
        DESCRIPTION: Check Build Your Bet bet
        DESCRIPTION: displaying
        EXPECTED: * Won / Lost indicators(ticks/crosses) are displayed for the final result for each selection
        EXPECTED: * Progress bars are NOT displayed anymore for selections with **Range** template
        EXPECTED: * Final result for stats descriptions are shown (e.g. 2 Goals, 49 Passes) for selections with **Range** template
        EXPECTED: ![](index.php?/attachments/get/114837485) ![](index.php?/attachments/get/114837490)
        """
        pass

    def test_005_check_the_same_byb_in_24_hours(self):
        """
        DESCRIPTION: Check the same BYB in 24 hours
        EXPECTED: * Won / Lost indicators(ticks/crosses) are displayed for the final result for each selection
        EXPECTED: * Progress bars are NOT displayed anymore for selections with **Range** template
        EXPECTED: * Final result for stats descriptions are not shown any longer (as this data is stored for 24 hrs)
        """
        pass

    def test_006_go_to_cash_out_tab_and_repeat_steps_1_4_coral_only(self):
        """
        DESCRIPTION: Go to Cash out tab and repeat steps #1-4 (Coral only)
        EXPECTED: 
        """
        pass

    def test_007_repeat_steps_1_5_for_5_a_side_bet(self):
        """
        DESCRIPTION: Repeat steps #1-5 for **5-a-side** bet
        EXPECTED: 
        """
        pass
