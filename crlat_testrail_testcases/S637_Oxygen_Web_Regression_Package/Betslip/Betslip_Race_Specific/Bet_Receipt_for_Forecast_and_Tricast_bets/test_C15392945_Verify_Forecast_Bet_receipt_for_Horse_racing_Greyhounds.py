import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C15392945_Verify_Forecast_Bet_receipt_for_Horse_racing_Greyhounds(Common):
    """
    TR_ID: C15392945
    NAME: Verify Forecast Bet receipt for Horse racing/Greyhounds
    DESCRIPTION: This test case verifies Forecastbet receipt for Horse Racing/Greyhound bets
    PRECONDITIONS: User logged in and Placed a Forecast bet in HorseRacing/Greyhound page
    """
    keep_browser_open = True

    def test_001_verify_forecast_bet_receipt_header(self):
        """
        DESCRIPTION: Verify Forecast Bet Receipt header
        EXPECTED: Bet Receipt header contains the following elements:
        EXPECTED: 'X' button
        EXPECTED: 'Bet Receipt' title
        EXPECTED: 'User Balance' button
        """
        pass

    def test_002_verify_forecast_bet_bet_receipt_subheader(self):
        """
        DESCRIPTION: Verify Forecast Bet Bet Receipt subheader
        EXPECTED: Bet Receipt subheader contains the following elements:
        EXPECTED: 'Check' icon and 'Bet Placed Successfully' text
        EXPECTED: Date and time in the next format: i.e. 19/09/2019, 14:57 and aligned by the right side
        EXPECTED: Bet count in the next format: 'Your Bets:(X)' where 'X' is the number of bets placed in for that receipt
        """
        pass

    def test_003_verify_forecast_bet_receiptindexphpattachmentsget31337(self):
        """
        DESCRIPTION: Verify Forecast bet receipt
        DESCRIPTION: ![](index.php?/attachments/get/31337)
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
        EXPECTED: 1st Drops of Jupitor
        EXPECTED: 2nd Massina
        EXPECTED: Forecast / 11:45 Chantilly (FR)
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
        EXPECTED: 1st Drops of Jupitor
        EXPECTED: 2nd Massina
        EXPECTED: Forecast / 11:45 Chantilly (FR)
        EXPECTED: 1 line at £0.10 per line
        EXPECTED: Stake for this bet: £1.00
        EXPECTED: Potential Returns: N/A
        EXPECTED: Total Stake £1.00
        EXPECTED: Reuse Selections
        EXPECTED: Go Betting
        """
        pass

    def test_004_place_a_combination_forecast_betverify_bet_receipt_card_in_the_betslip(self):
        """
        DESCRIPTION: Place a Combination Forecast bet
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
        EXPECTED: Combination Forecast / 11:45 Chantilly (FR)
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
        EXPECTED: Combination Forecast / 11:45 Chantilly (FR)
        EXPECTED: 1 line at £0.10 per line
        EXPECTED: Stake for this bet: £1.00
        EXPECTED: Potential Returns: N/A
        EXPECTED: Total Stake £1.00
        EXPECTED: Reuse Selections
        EXPECTED: Go Betting
        """
        pass

    def test_005_place_multiple_single_bets_and_check_the_bet_receipt(self):
        """
        DESCRIPTION: Place Multiple single bets and check the Bet receipt
        EXPECTED: Bet count information is updated according to the number of single bets Your bets (2)
        EXPECTED: Followed by Single bet cards in Order
        EXPECTED: At the End Total Stake and Estimated/Potential Returns
        EXPECTED: "
        """
        pass

    def test_006_verify_bet_id(self):
        """
        DESCRIPTION: Verify Bet ID
        EXPECTED: Bet ID corresponds to the value, received from OpenBet
        """
        pass

    def test_007_verify_stake__stake_for_this_bet(self):
        """
        DESCRIPTION: Verify Stake / Stake for this bet
        EXPECTED: Total stake value corresponds to the actual total stake based on the stake value entered
        """
        pass

    def test_008_verify_est_returns__potential_returns(self):
        """
        DESCRIPTION: Verify Est. Returns / Potential Returns
        EXPECTED: Est. Returns/Potential value is "N/A"
        """
        pass

    def test_009_verify_total_stake_and_estpotential_returns_at_the_bottom_of_the_betslip(self):
        """
        DESCRIPTION: Verify Total Stake and Est./Potential Returns at the bottom of the betslip
        EXPECTED: * Total Stake value corresponds to the actual total stake based on the stake value entered
        EXPECTED: * Est./Potential Returns value is "N/A"
        """
        pass

    def test_010_click_on_reuse_selection_button(self):
        """
        DESCRIPTION: Click on 'Reuse Selection' button
        EXPECTED: Forecast bet appears in the BetSlip again
        """
        pass

    def test_011_place_forecast_bet_again(self):
        """
        DESCRIPTION: Place Forecast bet again
        EXPECTED: * Forecast bet is placed successfully
        EXPECTED: * Bet Receipt appears
        """
        pass
