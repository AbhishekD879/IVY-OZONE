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
class Test_C2320927_Verify_UK_Tote_Jackpot_Bet_Receipt(Common):
    """
    TR_ID: C2320927
    NAME: Verify UK Tote Jackpot Bet Receipt
    DESCRIPTION: This test case verifies Jackpot Bet Receipt, which appears in betslip after the user has placed an Jackpot Tote bet
    DESCRIPTION: Please note that we are **NOT** **ALLOWED** to Place a Tote bets on HL and PROD environments!
    DESCRIPTION: AUTOTEST C2604459
    PRECONDITIONS: * The User's account balance is sufficient to cover the bet stake
    PRECONDITIONS: * User is logged in
    PRECONDITIONS: * UK Tote feature is enabled in CMS
    PRECONDITIONS: * Jackpot pool type is available for HR Event
    PRECONDITIONS: * **User should have placed an Jackpot Tote bet**
    PRECONDITIONS: To load Totepool ON/OFF CMS config use System-configuration (https://coral-cms- **endpoint** .symphony-solutions.eu)
    PRECONDITIONS: **endpoint** can be found using devlog
    """
    keep_browser_open = True

    def test_001_verify_jackpot_tote_bet_receipt_header(self):
        """
        DESCRIPTION: Verify Jackpot Tote Bet Receipt header
        EXPECTED: Bet Receipt header contains the following elements:
        EXPECTED: * 'X' button
        EXPECTED: * 'Bet Receipt' title
        EXPECTED: * 'User Balance' button
        """
        pass

    def test_002_verify_jackpot_tote_bet_receipt_subheader(self):
        """
        DESCRIPTION: Verify Jackpot Tote Bet Receipt subheader
        EXPECTED: Bet Receipt subheader contains the following elements:
        EXPECTED: * 'Check' icon and 'Bet Placed Successfully' text
        EXPECTED: * Date and time in the next format: i.e. 19/09/2019, 14:57 and aligned by the right side
        EXPECTED: * Bet count in the next format: 'Your Bets:(X)' where 'X' is the number of bets placed in for that receipt
        """
        pass

    def test_003_verify_jackpot_tote_bet_receipt_in_the_bet_slip(self):
        """
        DESCRIPTION: Verify Jackpot Tote bet receipt in the bet slip
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
        EXPECTED: 5. Kingston Mimosa
        EXPECTED: 6. Midnight Owle
        EXPECTED: Leg 1 - 15:25 Taunton
        EXPECTED: 1. Oxwich Bay
        EXPECTED: 2. On The Rox
        EXPECTED: Leg 2 - 16:00 Taunton
        EXPECTED: 2. Pobbles Bay
        EXPECTED: Leg 3 - 16:30 Taunton
        EXPECTED: 3. Gonnabegood
        EXPECTED: 7. Mr Magill
        EXPECTED: Leg 4 - 17:05 Taunton
        EXPECTED: 3. Gonnabegood
        EXPECTED: Leg 5 - 17:10 Taunton
        EXPECTED: 3. Gonnabegood
        EXPECTED: Leg 6 - 17:15 Taunton
        EXPECTED: Jackpot Totepool / 1 Line at £2 per line
        EXPECTED: Stake: £2
        EXPECTED: Est. Returns: N/A
        EXPECTED: Total Stake £2
        EXPECTED: Estimated Returns N/A
        EXPECTED: Reuse Selection
        EXPECTED: Go Betting
        EXPECTED: Ladbrokes:
        EXPECTED: Single
        EXPECTED: Receipt No: O/17781521/0000041
        EXPECTED: 2. Drops of Jupitor
        EXPECTED: 5. Kingston Mimosa
        EXPECTED: 6. Midnight Owle
        EXPECTED: Leg 1 - 15:25 Taunton
        EXPECTED: 1. Oxwich Bay
        EXPECTED: 2. On The Rox
        EXPECTED: Leg 2 - 16:00 Taunton
        EXPECTED: 2. Pobbles Bay
        EXPECTED: Leg 3 - 16:30 Taunton
        EXPECTED: 3. Gonnabegood
        EXPECTED: 7. Mr Magill
        EXPECTED: Leg 4 - 17:05 Taunton
        EXPECTED: 3. Gonnabegood
        EXPECTED: Leg 5 - 17:10 Taunton
        EXPECTED: 3. Gonnabegood
        EXPECTED: Leg 6 - 17:15 Taunton
        EXPECTED: Jackpot Totepool / 1 Line at £2 per line
        EXPECTED: Stake for this bet: £2
        EXPECTED: Potential Returns: N/A
        EXPECTED: Total Stake £2
        EXPECTED: Reuse Selections
        EXPECTED: Go Betting
        """
        pass

    def test_004_verify_total_stake(self):
        """
        DESCRIPTION: Verify Total Stake
        EXPECTED: Total stake value corresponds to the actual total stake based on the stake value entered
        """
        pass

    def test_005_verify_est_returns(self):
        """
        DESCRIPTION: Verify Est. Returns
        EXPECTED: Est. Returns value is "N/A"
        """
        pass

    def test_006_click_on_reuse_selection_button(self):
        """
        DESCRIPTION: Click on 'Reuse Selection' button
        EXPECTED: * "Jackpot Totepool" bet appears in the BetSlip again
        EXPECTED: * Previous stake value is entered
        """
        pass

    def test_007_place_a_jackpot_bet_again(self):
        """
        DESCRIPTION: Place a Jackpot bet again
        EXPECTED: * Jackpot Totepool is placed successfully
        EXPECTED: * Bet Receipt appears
        """
        pass

    def test_008_tap_the_go_betting_button(self):
        """
        DESCRIPTION: Tap the "Go betting" button
        EXPECTED: * Bet receipt is removed from the betslip
        EXPECTED: * Betslip is closed
        EXPECTED: * User is on racecard
        """
        pass
