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
class Test_C60347158_Verify_Bet_Tracker_info_when_the_bet_has_been_cashed_out(Common):
    """
    TR_ID: C60347158
    NAME: Verify Bet Tracker info when the bet has been cashed out
    DESCRIPTION: This test case verifies Bet Tracker info when user makes cashout
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

    def test_002_make_a_cashout(self):
        """
        DESCRIPTION: Make a cashout
        EXPECTED: * Bet with cashout event disappears from 'Open Bets'/'Cashout' tab/page
        """
        pass

    def test_003_go_to_settled_bets_tab(self):
        """
        DESCRIPTION: Go to 'Settled bets' tab
        EXPECTED: * 'Settled bets' tab is opened
        EXPECTED: * Status for Event is received from OpenBet
        """
        pass

    def test_004_check_build_your_bet_betdisplaying(self):
        """
        DESCRIPTION: Check Build Your Bet bet
        DESCRIPTION: displaying
        EXPECTED: * Won / Lost indicators(ticks/crosses) are displayed for the final result for each selection settled in OB
        EXPECTED: * Winning / Losing indicators are displayed for selections not settled in OB
        EXPECTED: * Progress bars are NOT displayed anymore for selections with **Range** template
        EXPECTED: * Final result for stats descriptions are shown (e.g. 2 Goals, 49 Passes) for selections with **Range** template
        """
        pass

    def test_005_repeat_steps_1_4_for_5_a_side_bet(self):
        """
        DESCRIPTION: Repeat steps #1-4 for **5-a-side** bet
        EXPECTED: 
        """
        pass
