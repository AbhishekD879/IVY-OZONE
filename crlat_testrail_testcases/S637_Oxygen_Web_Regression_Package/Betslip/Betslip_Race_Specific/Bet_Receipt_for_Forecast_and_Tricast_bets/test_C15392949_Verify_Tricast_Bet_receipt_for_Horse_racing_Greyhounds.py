import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.races
@vtest
class Test_C15392949_Verify_Tricast_Bet_receipt_for_Horse_racing_Greyhounds(Common):
    """
    TR_ID: C15392949
    NAME: Verify Tricast Bet receipt for Horse racing/Greyhounds
    DESCRIPTION: This test case verifies Tricast bet receipt for Horse Racing/Greyhound bets
    PRECONDITIONS: User logged in and Placed a Tricast bet in HorseRacing/Greyhound page
    """
    keep_browser_open = True

    def test_001_verify_tricast_bet_receipt_header(self):
        """
        DESCRIPTION: Verify Tricast Bet Receipt header
        EXPECTED: Bet Receipt header contains the following elements:
        EXPECTED: 'X' button
        EXPECTED: 'Bet Receipt' title
        EXPECTED: 'User Balance' button
        """
        pass

    def test_002_verify_tricast_bet_bet_receipt_subheader(self):
        """
        DESCRIPTION: Verify Tricast Bet Bet Receipt subheader
        EXPECTED: Bet Receipt subheader contains the following elements:
        EXPECTED: 'Check' icon and 'Bet Placed Successfully' text
        EXPECTED: Date and time in the next format: i.e. 19/09/2019, 14:57 and aligned by the right side
        EXPECTED: Bet count in the next format: 'Your Bets:(X)' where 'X' is the number of bets placed in for that receipt
        """
        pass

    def test_003_verify_tricast_bet_receipt(self):
        """
        DESCRIPTION: Verify Tricast bet receipt
        EXPECTED: The following information is displayed on the bet receipt:
        EXPECTED: Bet type name
        EXPECTED: Bet ID
        EXPECTED: Selection name
        EXPECTED: Bet Type name / Meeting
        EXPECTED: Stake - Stake on this Bet / Estimated - Potential Returns
        EXPECTED: Total Stake / Estimate - Potential Returns
        EXPECTED: Coral:
        EXPECTED: Single @SP
        EXPECTED: Bet ID: 0/17781521/0000041
        EXPECTED: 1st. Drops of Jupitor
        EXPECTED: 2nd. Massina
        EXPECTED: 3rd. Embour
        EXPECTED: Tricast / 11:45 Chantilly (FR)
        EXPECTED: 1 line at £0.10 per line
        EXPECTED: Stake: £0.10
        EXPECTED: Est. Returns: N/A
        EXPECTED: Total Stake £0.10
        EXPECTED: Estimated Returns N/A
        EXPECTED: Reuse Selection
        EXPECTED: Go Betting
        EXPECTED: Ladbrokes:
        EXPECTED: Single @SP
        EXPECTED: Receipt No: O/17781521/0000041
        EXPECTED: 1st. Drops of Jupitor
        EXPECTED: 2nd. Massina
        EXPECTED: 3rd. Embour
        EXPECTED: Tricast / 11:45 Chantilly (FR)
        EXPECTED: 1 line at £0.10 per line
        EXPECTED: Stake for this bet: £1.00
        EXPECTED: Potential Returns: N/A
        EXPECTED: Total Stake £1.00
        EXPECTED: Reuse Selections
        EXPECTED: Go Betting
        """
        pass

    def test_004_place_a_combination_tricast_betverify_bet_receipt_card_in_the_betslip(self):
        """
        DESCRIPTION: Place a Combination Tricast bet
        DESCRIPTION: Verify bet receipt card in the betslip
        EXPECTED: The following information is displayed on the bet receipt:
        EXPECTED: Bet type name
        EXPECTED: Bet ID
        EXPECTED: Selection name
        EXPECTED: Bet Type name / Meeting
        EXPECTED: Stake - Stake on this Bet / Estimated - Potential Returns
        EXPECTED: Total Stake / Estimate - Potential Returns
        EXPECTED: Coral:
        EXPECTED: Single @SP
        EXPECTED: Bet ID: 0/17781521/0000041
        EXPECTED: Drops of Jupitor
        EXPECTED: Massina
        EXPECTED: Massina 1
        EXPECTED: Combination Tricast / 11:45 Chantilly (FR)
        EXPECTED: 1 line at £0.10 per line
        EXPECTED: Stake: £0.10
        EXPECTED: Est. Returns: N/A
        EXPECTED: Total Stake £0.10
        EXPECTED: Estimated Returns N/A
        EXPECTED: Reuse Selection
        EXPECTED: Go Betting
        EXPECTED: Ladbrokes:
        EXPECTED: Single @SP
        EXPECTED: Receipt No: O/17781521/0000041
        EXPECTED: Drops of Jupitor
        EXPECTED: Massina
        EXPECTED: Massina 1
        EXPECTED: Combination Tricast / 11:45 Chantilly (FR)
        EXPECTED: 1 line at £0.10 per line
        EXPECTED: Stake for this bet: £1.00
        EXPECTED: Potential Returns: N/A
        EXPECTED: Total Stake £1.00
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

    def test_006_verify_stake__stake_for_this_bet(self):
        """
        DESCRIPTION: Verify Stake / Stake for this bet
        EXPECTED: Total stake value corresponds to the actual total stake based on the stake value entered
        """
        pass

    def test_007_verify_est_returns__potential_returns(self):
        """
        DESCRIPTION: Verify Est. Returns / Potential Returns
        EXPECTED: Est. Returns/Potential value is "N/A"
        """
        pass

    def test_008_verify_total_stake_and_estpotential_returns_at_the_bottom_of_the_betslip(self):
        """
        DESCRIPTION: Verify Total Stake and Est./Potential Returns at the bottom of the betslip
        EXPECTED: * Total Stake value corresponds to the actual total stake based on the stake value entered
        EXPECTED: * Est./Potential Returns value is "N/A"
        """
        pass

    def test_009_click_on_the_reuse_selection_button(self):
        """
        DESCRIPTION: Click on the 'Reuse Selection' button
        EXPECTED: Tricast bet appears in the BetSlip again
        """
        pass

    def test_010_place_tricast_bet_again(self):
        """
        DESCRIPTION: Place Tricast bet again
        EXPECTED: * Tricast bet is placed successfully
        EXPECTED: * Bet Receipt appears
        """
        pass
