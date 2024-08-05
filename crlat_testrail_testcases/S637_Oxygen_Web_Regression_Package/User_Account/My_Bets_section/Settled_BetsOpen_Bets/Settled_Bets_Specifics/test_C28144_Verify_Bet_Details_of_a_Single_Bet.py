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
class Test_C28144_Verify_Bet_Details_of_a_Single_Bet(Common):
    """
    TR_ID: C28144
    NAME: Verify Bet Details of a Single Bet
    DESCRIPTION: This test case verifies Bet Details of a Single Bet
    PRECONDITIONS: 1. User should be logged in to view their settled bets
    PRECONDITIONS: 2. User should have few won/lost/void/cashed out Single bets
    PRECONDITIONS: No cashout for PM bets according to https://jira.egalacoral.com/browse/BMA-52721
    """
    keep_browser_open = True

    def test_001_navigate_to_settled_bets_tab_on_my_bets_page_for_mobile(self):
        """
        DESCRIPTION: Navigate to 'Settled Bets' tab on 'My Bets' page (for mobile)
        EXPECTED: * 'Settled Bets' tab is opened
        EXPECTED: * Won/lost/void/cashed out bet overview sections are present
        """
        pass

    def test_002_verify_bet_with_won_status(self):
        """
        DESCRIPTION: Verify bet with **WON** status
        EXPECTED: The following information is shown in the bet overview:
        EXPECTED: **For** **98** **Release**:
        EXPECTED: * Bet type and green "WON" label
        EXPECTED: * Selection name user has bet on
        EXPECTED: * Odds of selection and green "WON" label
        EXPECTED: * Date of placing the bet and bet receipt ID
        EXPECTED: * Market name user has bet on - e.g., Win or Each Way
        EXPECTED: * Event name and final scores (if available)
        EXPECTED: * Date of bet placement and bet receipt ID are shown below bet details
        EXPECTED: * Stake <currency symbol> <value> (e.g., £10.00)
        EXPECTED: * Est. Returns <currency symbol> <value> (e.g., £30.00)
        EXPECTED: **For** **99** **Release**:
        EXPECTED: * Bet type and "WON" label (in the header)
        EXPECTED: * 'You won <currency sign and value>' label right under header, on top of event card is shown
        EXPECTED: *green tick icon on the left of the selection
        EXPECTED: * Selection name user has bet on
        EXPECTED: * Odds of selection displayed through @ symbol next to selection name (eg. Home@1/4)
        EXPECTED: * Market name user has bet on - e.g., Win or Each Way
        EXPECTED: * Event name and final scores (if available)/event time (on same level)
        EXPECTED: * Stake <currency symbol> <value> (e.g., £10.00) on the left (in the footer)
        EXPECTED: * Est. Returns <currency symbol> <value> (e.g., £30.00) next to stake value
        EXPECTED: * Date of bet placement and bet receipt ID are shown below stake value (in the footer)
        """
        pass

    def test_003_verify_bet_with_lost_status(self):
        """
        DESCRIPTION: Verify bet with **LOST** status
        EXPECTED: The following information is shown in the bet overview:
        EXPECTED: **For** **98** **Release**:
        EXPECTED: * Bet type and grey "LOST" label (in the header)
        EXPECTED: * Selection name user has bet on
        EXPECTED: * Odds of selection and green "WON" label
        EXPECTED: * Date of placing the bet and bet receipt ID
        EXPECTED: * Market name user has bet on - e.g., Win or Each Way
        EXPECTED: * Event name and final scores (if available)
        EXPECTED: * Date of bet placement and bet receipt ID are shown below bet details
        EXPECTED: * Stake <currency symbol> <value> (e.g., £10.00)
        EXPECTED: * Est. Returns <currency symbol> <value> (£0.00 for LOST)
        EXPECTED: **For** **99** **Release**:
        EXPECTED: * Bet type and "LOST" label (in the header)
        EXPECTED: *red cross icon on the left of the selection
        EXPECTED: * Selection name user has bet on
        EXPECTED: * Odds of selection displayed through @ symbol next to selection name (eg. Home@1/4)
        EXPECTED: * Market name user has bet on - e.g., Win or Each Way
        EXPECTED: * Event name and final scores (if available)/event time (on same level)
        EXPECTED: * Stake <currency symbol> <value> (e.g., £10.00) on the left (in the footer)
        EXPECTED: * Est. Returns <currency symbol> <value> (£0.00 for LOST) next to stake value
        EXPECTED: * Date of bet placement and bet receipt ID are shown below stake value (in the footer)
        """
        pass

    def test_004_verify_bet_with_void_status(self):
        """
        DESCRIPTION: Verify bet with **VOID** status
        EXPECTED: The following information is shown in the bet overview:
        EXPECTED: **For** **98** **Release**:
        EXPECTED: * Bet type and "VOID" label (in the header)
        EXPECTED: * Selection name user has bet on
        EXPECTED: * Odds of selection and green "WON" label
        EXPECTED: * Date of placing the bet and bet receipt ID
        EXPECTED: * Market name user has bet on - e.g., Win or Each Way
        EXPECTED: * Event name and final scores (if available)
        EXPECTED: * Date of bet placement and bet receipt ID are shown below bet details
        EXPECTED: * Stake <currency symbol> <value> (e.g., £10.00)
        EXPECTED: * Est. Returns <currency symbol> <value> (e.g., £30.00)
        EXPECTED: **For** **99** **Release**:
        EXPECTED: * Bet type and "VOID" label (in the header)
        EXPECTED: * VOID label on the left of the selection
        EXPECTED: * Selection name user has bet on
        EXPECTED: * Odds of selection displayed through @ symbol next to selection name (eg. Home@1/4)
        EXPECTED: * Market name user has bet on - e.g., Win or Each Way
        EXPECTED: * Event name and final scores (if available)/event time (on same level)
        EXPECTED: * Stake <currency symbol> <value> (e.g., £10.00) on the left (in the footer)
        EXPECTED: * Est. Returns <currency symbol> <value> (e.g., £30.00) next to stake value
        EXPECTED: * Date of bet placement and bet receipt ID are shown below stake value (in the footer)
        """
        pass

    def test_005_verify_bet_with_cashed_out_status(self):
        """
        DESCRIPTION: Verify bet with **CASHED OUT** status
        EXPECTED: The following information is shown in the bet overview:
        EXPECTED: **For** **98** **Release**:
        EXPECTED: * Bet type and green "CASHED OUT" label
        EXPECTED: * Selection name user has bet on
        EXPECTED: * Odds of selection and green "WON" label
        EXPECTED: * Date of placing the bet and bet receipt ID
        EXPECTED: * Market name user has bet on - e.g., Win or Each Way
        EXPECTED: * Event name and final scores (if available)
        EXPECTED: * Date of bet placement and bet receipt ID are shown below bet details
        EXPECTED: * Stake <currency symbol> <value> (e.g., £10.00)
        EXPECTED: * Est. Returns <currency symbol> <value> (e.g., £30.00)
        EXPECTED: **For** **99** **Release**:
        EXPECTED: * Bet type and "CASHED OUT" label (in the header)
        EXPECTED: * Selection name user has bet on
        EXPECTED: * Odds of selection displayed through @ symbol next to selection name (eg. Home@1/4)
        EXPECTED: * Market name user has bet on - e.g., Win or Each Way
        EXPECTED: * Event name and final scores (if available)/event time (on same level)
        EXPECTED: * Stake <currency symbol> <value> (e.g., £10.00) on the left (in the footer)
        EXPECTED: * Est. Returns <currency symbol> <value> (e.g., £30.00) next to stake value
        EXPECTED: * Date of bet placement and bet receipt ID are shown below stake value (in the footer)
        """
        pass

    def test_006_verify_long_names_on_settled_bets_card(self):
        """
        DESCRIPTION: Verify long names on Settled Bets card
        EXPECTED: * Long name of a selection is fully displayed
        EXPECTED: * Long name of a market is fully displayed
        EXPECTED: * Long name of an event is fully displayed
        """
        pass

    def test_007_repeat_this_test_case_for_a_bet_placed_on_private_market_except_cashed_out_status_because_cashout_is_not_offered_for_bets_placed_on_private_market_selections(self):
        """
        DESCRIPTION: Repeat this test case for a bet placed on Private Market (except cashed out status, because cashout is not offered for bets placed on private market selections)
        EXPECTED: 
        """
        pass

    def test_008_repeat_steps_2_6_for_settled_bets_tab_account_history_page_for_mobile_bet_slip_widget_for_tabletdesktop(self):
        """
        DESCRIPTION: Repeat steps 2-6 for:
        DESCRIPTION: * 'Settled Bets' tab 'Account History' page (for mobile)
        DESCRIPTION: * 'Bet Slip' widget (for Tablet/Desktop)
        EXPECTED: 
        """
        pass
