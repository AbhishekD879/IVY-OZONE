import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.critical
@pytest.mark.bet_history_open_bets
@vtest
class Test_C1358436_Verify_Bet_Details_of_a_Single_Horse_Racing_bet(Common):
    """
    TR_ID: C1358436
    NAME: Verify Bet Details of a Single Horse Racing bet
    DESCRIPTION: This test case verifies bet details of a single horse racing bet
    DESCRIPTION: AUTOTEST [C2302119]
    PRECONDITIONS: 1. User should be logged in to view their settled bets.
    PRECONDITIONS: 2. User should have Single horse racing bets placed with each way and without. The bets are already settled
    """
    keep_browser_open = True

    def test_001_navigate_to_settled_bets_tab_on_my_bets(self):
        """
        DESCRIPTION: Navigate to 'Settled Bets' tab on 'My Bets'
        EXPECTED: * 'Settled Bets' tab is opened
        """
        pass

    def test_002_verify_bet_details_of_a_single_horse_racing_bet_each_way(self):
        """
        DESCRIPTION: Verify bet details of a Single Horse Racing bet (each way)
        EXPECTED: The following bet details are shown:
        EXPECTED: * Bet type (e.g., "Single (Each Way)") on the header
        EXPECTED: * Result (Won/Lost/Void/Cashed out) on the header on the right
        EXPECTED: * If bet has won the message 'You won <currency symbol><value>' is displayed on the left, under event card header with green tick icon shown before message
        EXPECTED: * Selection name (with silks on the left of each selection if available)
        EXPECTED: * Odds placed next to selection name displayed through @ symbol (eg. @1/2, @SP)
        EXPECTED: * Market name user has bet on and Each Way terms (e.g., "Win or Each Way, 1/4 odds - places 1,2,3,4")
        EXPECTED: * Event name
        EXPECTED: * Result icon (if won-green tick, if lost-red cross, if void-void label) on the left of the selection, centered
        EXPECTED: * Unit stake <currency symbol> <value> (e.g., £10.00)
        EXPECTED: * Total stake <currency symbol> <value> (e.g., £20.00)
        EXPECTED: * Total returns <currency symbol> <value> (e.g., £30.00)
        EXPECTED: * Date of bet placement on the right
        EXPECTED: * Bet receipt ID shown below bet details on the left
        """
        pass

    def test_003_verify_bet_details_of_a_single_horse_racing_bet_no_each_way(self):
        """
        DESCRIPTION: Verify bet details of a Single Horse Racing bet (NO each way)
        EXPECTED: The following bet details are shown:
        EXPECTED: * Bet type (e.g., "Single") on the header
        EXPECTED: * Result (Won/Lost/Void/Cashed out) on the header on the right
        EXPECTED: * If bet has won the message 'You won <currency symbol><value>' is displayed on the left, under event card header with green tick icon shown before message
        EXPECTED: * Selection name (with silks on the left of each selection if available)
        EXPECTED: * Odds placed next to selection name displayed through @ symbol (eg. @1/2, @SP)
        EXPECTED: * Market name user has bet on - e.g., "Win or Each Way")
        EXPECTED: * Event name
        EXPECTED: * Result icon (if won-green tick, if lost-red cross, if void-void label) on the left of the selection, centered
        EXPECTED: * Stake <currency symbol> <value> (e.g., £20.00)
        EXPECTED: * Total returns <currency symbol> <value> (e.g., £40.00)
        EXPECTED: * Date of bet placement is shown on the right
        EXPECTED: * Bet receipt ID shown on the left
        """
        pass

    def test_004_repeat_steps_2_4_forcoral_only_settled_bets_tab_account_history_page_for_mobile_tap_on_user_icon_and_from_menu_select_history___betting_history___settled_bets_tab_will_be_opened_bet_slip_widget_for_tablet_and_desktop(self):
        """
        DESCRIPTION: Repeat steps 2-4 for:
        DESCRIPTION: Coral Only:
        DESCRIPTION: * 'Settled Bets' tab 'Account History' page (for mobile): tap on user icon and from Menu select 'History -> Betting history' - 'Settled Bets' tab will be opened
        DESCRIPTION: * 'Bet Slip' widget (for Tablet and Desktop)
        EXPECTED: 
        """
        pass
