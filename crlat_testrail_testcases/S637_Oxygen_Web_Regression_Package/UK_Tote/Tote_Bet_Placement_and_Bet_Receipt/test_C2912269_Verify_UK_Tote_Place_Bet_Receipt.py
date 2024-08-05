import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.races
@vtest
class Test_C2912269_Verify_UK_Tote_Place_Bet_Receipt(Common):
    """
    TR_ID: C2912269
    NAME: Verify UK Tote Place Bet Receipt
    DESCRIPTION: This test case verifies Place bet receipt, which appears in betslip after the user has placed an Place Tote bet
    DESCRIPTION: Please note that we are **NOT** **ALLOWED** to Place a Tote bets on HL and PROD environments!
    PRECONDITIONS: * The User's account balance is sufficient to cover the bet stake
    PRECONDITIONS: * User is logged in
    PRECONDITIONS: * UK Tote feature is enabled in CMS
    PRECONDITIONS: * Place pool type is available for HR Event
    PRECONDITIONS: * **User should have placed an Place Tote bet**
    PRECONDITIONS: To load Totepool ON/OFF CMS config use System-configuration (https://coral-cms- **endpoint** .symphony-solutions.eu)
    PRECONDITIONS: **endpoint** can be found using devlog
    """
    keep_browser_open = True

    def test_001_verify_place_tote_bet_receipt_header(self):
        """
        DESCRIPTION: Verify Place Tote Bet Receipt header
        EXPECTED: Bet Receipt header contains the following elements:
        EXPECTED: * 'X' button
        EXPECTED: * 'Bet Receipt' title
        EXPECTED: * 'User Balance' button
        """
        pass

    def test_002_verify_place_tote_bet_receipt_subheader(self):
        """
        DESCRIPTION: Verify Place Tote Bet Receipt subheader
        EXPECTED: Bet Receipt subheader contains the following elements:
        EXPECTED: * 'Check' icon and 'Bet Placed Successfully' text
        EXPECTED: * Date and time in the next format: i.e. 19/09/2019, 14:57 and aligned by the right side
        EXPECTED: * Bet count in the next format: 'Your Bets:(X)' where 'X' is the number of bets placed in for that receipt
        """
        pass

    def test_003_verify_place_tote_bet_receipt_for_place_bet_with_1_selection_in_the_betslip(self):
        """
        DESCRIPTION: Verify Place Tote bet receipt for Place Bet with 1 selection in the betslip
        EXPECTED: The following information is displayed on the bet receipt:
        EXPECTED: Bet type name
        EXPECTED: Bet ID
        EXPECTED: Selection name
        EXPECTED: Bet Type name / Meeting
        EXPECTED: Stake - Stake on this Bet / Estimated - Potential Returns
        EXPECTED: Total Stake / Estimate - Potential Returns
        EXPECTED: Coral:
        EXPECTED: Single
        EXPECTED: Bet ID: 0/17781521/0000041
        EXPECTED: 2. Drops of Jupitor
        EXPECTED: Place Totepool / 11:45 Chantilly (FR)
        EXPECTED: 1 line at £0.10 per line
        EXPECTED: Stake: £0.10
        EXPECTED: Est. Returns: N/A
        EXPECTED: Total Stake £0.10
        EXPECTED: Estimated Returns N/A
        EXPECTED: Reuse Selection
        EXPECTED: Go Betting
        EXPECTED: Ladbrokes:
        EXPECTED: Single
        EXPECTED: Receipt No: O/17781521/0000041
        EXPECTED: 2. Drops of Jupitor
        EXPECTED: Place Totepool / 11:45 Chantilly (FR)
        EXPECTED: 1 line at £0.10 per line
        EXPECTED: Stake for this bet: £1.00
        EXPECTED: Potential Returns: N/A
        EXPECTED: Total Stake £1.00
        EXPECTED: Reuse Selections
        EXPECTED: Go Betting
        """
        pass

    def test_004_verify_bet_id(self):
        """
        DESCRIPTION: Verify Bet ID
        EXPECTED: Bet ID corresponds to the value, received from OpenBet
        """
        pass

    def test_005_verify_total_stake(self):
        """
        DESCRIPTION: Verify Total Stake
        EXPECTED: Total stake value corresponds to the actual total stake based on the stake value entered
        """
        pass

    def test_006_verify_est_returnspotential_return(self):
        """
        DESCRIPTION: Verify Est. Returns/Potential Return
        EXPECTED: Est. Returns/Potential return value is "N/A"
        """
        pass

    def test_007_verify_total_stake_and_estpotential_returns_at_the_bottom_of_the_betslip(self):
        """
        DESCRIPTION: Verify Total Stake and Est./Potential Returns at the bottom of the betslip
        EXPECTED: * Total Stake value corresponds to the actual total stake based on the stake value entered
        EXPECTED: * Est./Potential Returns value is "N/A"
        """
        pass

    def test_008_click_on_reuse_selection_button(self):
        """
        DESCRIPTION: Click on 'Reuse Selection' button
        EXPECTED: "Place Totepool" bet appears in the BetSlip again
        """
        pass

    def test_009_place_a_place_bet_again(self):
        """
        DESCRIPTION: Place a 'Place' bet again
        EXPECTED: * Place Totepool bet is placed successfully
        EXPECTED: * Bet Receipt appears
        """
        pass

    def test_010_tap_the_go_betting_button(self):
        """
        DESCRIPTION: Tap the "Go betting" button
        EXPECTED: * Bet receipt is removed from the betslip
        EXPECTED: * Betslip is closed
        EXPECTED: * Previously visited page is shown
        """
        pass