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
class Test_C15785354_Verify_Forecast_and_Tricast_Bet_receipt_using_free_bets_for_Horse_Racing(Common):
    """
    TR_ID: C15785354
    NAME: Verify Forecast and Tricast Bet receipt using free bets for Horse Racing
    DESCRIPTION: This test case verifies Forecast and Tricast bet receipt for Horse Racing when free bets token is used while placing the bet.
    PRECONDITIONS: User logged in and has placed a Forecast and Tricast bet in Horse Racing using free bets token.
    """
    keep_browser_open = True

    def test_001_verify_forecast_bet_receipt_header(self):
        """
        DESCRIPTION: Verify Forecast Bet Receipt header.
        EXPECTED: Bet Receipt header contains the following elements:
        EXPECTED: 'X' button
        EXPECTED: 'Bet Receipt' title
        EXPECTED: 'User Balance' button
        """
        pass

    def test_002_verify_forecast_bet_bet_receipt_sub_header(self):
        """
        DESCRIPTION: Verify Forecast Bet Bet Receipt sub header.
        EXPECTED: Bet Receipt sub header contains the following elements:
        EXPECTED: 'Check' icon and 'Bet Placed Successfully' text.
        EXPECTED: Date and time in the format: i.e. 19/09/2019, 14:57 and aligned by the right side.
        EXPECTED: Bet count in the format: 'Your Bets:(X)' where 'X' is the number of bets placed in for that receipt.
        """
        pass

    def test_003_verify_forecast_bet_receipt_placed_using_free_bet_token(self):
        """
        DESCRIPTION: Verify Forecast bet receipt placed using free bet token.
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
        EXPECTED: Free Bet Amount: -'freebet value'
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
        EXPECTED: Free Bet Amount: -'freebet value'
        EXPECTED: Potential Returns: N/A
        EXPECTED: Total Stake £1.00
        EXPECTED: Reuse Selections
        EXPECTED: Go Betting
        """
        pass

    def test_004_place_multiple_single_bets_and_check_the_bet_receipt(self):
        """
        DESCRIPTION: Place Multiple single bets and check the Bet receipt.
        EXPECTED: Bet count information is updated according to the number of single bets Your bets (2)
        EXPECTED: Followed by Single bet cards in Order
        EXPECTED: At the End Total Stake and Estimated/Potential Returns
        """
        pass

    def test_005_verify_bet_id(self):
        """
        DESCRIPTION: Verify Bet ID
        EXPECTED: Bet ID corresponds to the value, received from OpenBet
        """
        pass

    def test_006_click_on_reuse_selection_button(self):
        """
        DESCRIPTION: Click on 'Reuse Selection' button
        EXPECTED: Forecast bet appears in the BetSlip again
        """
        pass
