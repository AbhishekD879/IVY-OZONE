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
class Test_C2320911_Verify_UK_Tote_Trifecta_Bet_Receipt(Common):
    """
    TR_ID: C2320911
    NAME: Verify UK Tote Trifecta Bet Receipt
    DESCRIPTION: This test case verifies Trifecta bet receipt, which appears in betslip after the user has placed an Trifecta Tote bet
    DESCRIPTION: Please note that we are **NOT** **ALLOWED** to Place a Tote bets on HL and PROD environments!
    DESCRIPTION: AUTOTEST C2593043
    PRECONDITIONS: * The User's account balance is sufficient to cover the bet stake
    PRECONDITIONS: * User is logged in
    PRECONDITIONS: * UK Tote feature is enabled in CMS
    PRECONDITIONS: * Trifecta pool types are available for HR Event
    PRECONDITIONS: * **User should have placed an Trifecta Tote bet**
    PRECONDITIONS: To load Totepool ON/OFF CMS config use System-configuration (https://coral-cms- **endpoint** .symphony-solutions.eu)
    PRECONDITIONS: **endpoint** can be found using devlog
    """
    keep_browser_open = True

    def test_001_verify_trifecta_tote_bet_receipt_header(self):
        """
        DESCRIPTION: Verify Trifecta Tote Bet Receipt header
        EXPECTED: Bet Receipt header contains the following elements:
        EXPECTED: * 'X' button
        EXPECTED: * 'Bet Receipt' title
        EXPECTED: * 'User Balance' button
        """
        pass

    def test_002_verify_trifecta_tote_bet_receipt_subheader(self):
        """
        DESCRIPTION: Verify Trifecta Tote Bet Receipt subheader
        EXPECTED: Bet Receipt subheader contains the following elements:
        EXPECTED: * 'Check' icon and 'Bet Placed Successfully' text
        EXPECTED: * Date and time in the next format: i.e. 19/09/2019, 14:57 and aligned by the right side
        EXPECTED: * Bet count in the next format: 'Your Bets:(X)' where 'X' is the number of bets placed in for that receipt
        """
        pass

    def test_003_verify_trifecta_tote_bet_receipt_for_1_trifecta_bet_in_the_betslip(self):
        """
        DESCRIPTION: Verify Trifecta Tote bet receipt for **1 Trifecta Bet** in the betslip
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
        EXPECTED: 5. Kingston
        EXPECTED: Trifecta Totepool / 11:45 Chantilly (FR)
        EXPECTED: 1 line at £2 per line
        EXPECTED: Stake: £0.10
        EXPECTED: Est. Returns: N/A
        EXPECTED: Total Stake £2
        EXPECTED: Estimated Returns N/A
        EXPECTED: Reuse Selection
        EXPECTED: Go Betting
        EXPECTED: Ladbrokes:
        EXPECTED: Single
        EXPECTED: Receipt No: O/17781521/0000041
        EXPECTED: 2. Drops of Jupitor
        EXPECTED: 5. Kingston
        EXPECTED: Trifecta Totepool / 11:45 Chantilly (FR)
        EXPECTED: 1 line at £2 per line
        EXPECTED: Stake for this bet: £12
        EXPECTED: Potential Returns: N/A
        EXPECTED: Total Stake £2
        EXPECTED: Reuse Selections
        EXPECTED: Go Betting
        """
        pass

    def test_004__place_a_combination_trifecta_tote_bet_verify_trifecta_tote_bet_receipt_for_combination_trifecta_in_the_betslip(self):
        """
        DESCRIPTION: * Place a **Combination Trifecta** tote bet
        DESCRIPTION: * Verify Trifecta Tote bet receipt for **Combination Trifecta** in the betslip
        EXPECTED: * "Singles (1)" label in the section header
        EXPECTED: * "Exacta Totepool" label --> Select Multiple ANY
        EXPECTED: * "x lines Combination Exacta" bet type name
        EXPECTED: * Corresponding selections with race card numbers next to them
        EXPECTED: WHERE
        EXPECTED: '#' of lines in Combination Exacta is calculated by the formula:
        EXPECTED: No. of selections x next lowest number (eg. 5 Selections picked 5 x 4 = 20)
        EXPECTED: * The following information is displayed on the bet receipt:
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
        EXPECTED: 5. Kingston Mimosa
        EXPECTED: 6. Midnight Owle
        EXPECTED: 8. American
        EXPECTED: Trifecta Totepool / 11:45 Chantilly (FR)
        EXPECTED: 24 lines at £1 per line
        EXPECTED: Stake: £24
        EXPECTED: Est. Returns: N/A
        EXPECTED: Total Stake £24
        EXPECTED: Estimated Returns N/A
        EXPECTED: Reuse Selection
        EXPECTED: Go Betting
        EXPECTED: Ladbrokes:
        EXPECTED: Single
        EXPECTED: Receipt No: O/17781521/0000041
        EXPECTED: 2. Drops of Jupitor
        EXPECTED: 5. Kingston Mimosa
        EXPECTED: 6. Midnight Owle
        EXPECTED: 8. American
        EXPECTED: Trifecta Totepool / 11:45 Chantilly (FR)
        EXPECTED: 24 lines at £1 per line
        EXPECTED: Stake for this bet: £24
        EXPECTED: Potential Returns: N/A
        EXPECTED: Total Stake £24
        EXPECTED: Reuse Selections
        EXPECTED: Go Betting
        """
        pass

    def test_005_verify_bet_id(self):
        """
        DESCRIPTION: Verify Bet ID
        EXPECTED: Bet ID corresponds to the value, received from OpenBet
        """
        pass

    def test_006_verify_total_stake(self):
        """
        DESCRIPTION: Verify Total Stake
        EXPECTED: Total stake value corresponds to the actual total stake based on the stake value entered
        """
        pass

    def test_007_verify_est_returnspotential_returns(self):
        """
        DESCRIPTION: Verify Est. Returns/Potential Returns
        EXPECTED: Est. Returns value/Potential Returns is "N/A"
        """
        pass

    def test_008_verify_total_stake_and_estpotential_returns_at_the_bottom_of_the_betslip(self):
        """
        DESCRIPTION: Verify Total Stake and Est./Potential Returns at the bottom of the betslip
        EXPECTED: * Total Stake value corresponds to the actual total stake based on the stake value entered
        EXPECTED: * Est./Potential Returns value is "N/A"
        """
        pass

    def test_009_click_on_reuse_selection_button(self):
        """
        DESCRIPTION: Click on 'Reuse Selection' button
        EXPECTED: "Trifecta" bet appears in the BetSlip again
        """
        pass

    def test_010_place_a_trifecta_bet_again(self):
        """
        DESCRIPTION: Place a Trifecta bet again
        EXPECTED: * Trifecta bet is placed successfully
        EXPECTED: * Bet Receipt appears
        """
        pass

    def test_011_tap_the_go_betting_button(self):
        """
        DESCRIPTION: Tap the "Go betting" button
        EXPECTED: * Bet receipt is removed from the betslip
        EXPECTED: * Betslip is closed
        EXPECTED: * Previously visited page is shown
        """
        pass
