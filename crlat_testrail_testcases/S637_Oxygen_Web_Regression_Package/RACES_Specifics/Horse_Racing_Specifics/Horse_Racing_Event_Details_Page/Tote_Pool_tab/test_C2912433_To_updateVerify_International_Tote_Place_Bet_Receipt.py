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
class Test_C2912433_To_updateVerify_International_Tote_Place_Bet_Receipt(Common):
    """
    TR_ID: C2912433
    NAME: [To update]Verify International Tote Place Bet Receipt
    DESCRIPTION: This test case verifies Place bet receipt, which appears in betslip after the user has placed an Place Tote bet
    DESCRIPTION: Please note that we are **NOT** **ALLOWED** to Place a Tote bets on HL and PROD environments!
    DESCRIPTION: AUTOTEST [C9864904]
    PRECONDITIONS: * The User's account balance is sufficient to cover the bet stake
    PRECONDITIONS: * User is logged in
    PRECONDITIONS: * International Tote feature is enabled in CMS
    PRECONDITIONS: * Place pool type is available for International HR Event
    PRECONDITIONS: * **User should have placed an Place Tote bet**
    """
    keep_browser_open = True

    def test_001_verify_place_for__international_tote_bet_receipt_header(self):
        """
        DESCRIPTION: Verify Place for  International Tote Bet Receipt Header
        EXPECTED: Bet Receipt header contains the following elements:
        EXPECTED: 'X' button
        EXPECTED: 'Bet Receipt' title
        EXPECTED: 'User Balance' button
        """
        pass

    def test_002_verify_place_international_tote_bet_receipt_subheader(self):
        """
        DESCRIPTION: Verify Place International Tote Bet Receipt subheader
        EXPECTED: Bet Receipt subheader contains the following elements:
        EXPECTED: 'Check' icon and 'Bet Placed Successfully' text
        EXPECTED: Date and time in the next format: i.e. 19/09/2019, 14:57 and aligned by the right side
        EXPECTED: Bet count in the next format: 'Your Bets:(X)' where 'X' is the number of bets placed in for that receipt
        """
        pass

    def test_003_verify_place_international_tote_bet_receipt_card_for_win_bet(self):
        """
        DESCRIPTION: Verify Place International Tote Bet Receipt card for Win Bet
        EXPECTED: The following information is displayed on the bet receipt card:
        EXPECTED: Bet type name ("Single" label in the section header)
        EXPECTED: Bet ID(Coral)/Receipt No(Ladbrokes)
        EXPECTED: Tote selections name Eg: 2nd Drops
        EXPECTED: (Leg & Meeting)  Time / Meeting  ( Leg 1  Win Totepool / 13.25 Place )
        EXPECTED: For Coral: Total Stake: /Est. Returns
        EXPECTED: For Ladbrokes: Stake for this Bet: /Potential Returns:
        """
        pass

    def test_004_verify_bet_id(self):
        """
        DESCRIPTION: Verify Bet ID
        EXPECTED: Bet ID corresponds to the value, received from OpenBet
        """
        pass

    def test_005_click_on_reuse_selection_button(self):
        """
        DESCRIPTION: Click on 'Reuse Selection' button
        EXPECTED: International "Place" bet appears in the BetSlip again
        """
        pass

    def test_006_place_a_place_bet_again(self):
        """
        DESCRIPTION: Place a 'Place' bet again
        EXPECTED: * Place bet is placed successfully
        EXPECTED: * Bet Receipt appears
        """
        pass

    def test_007_tap_the_done_button(self):
        """
        DESCRIPTION: Tap the "Done" button
        EXPECTED: * Bet receipt is removed from the betslip
        EXPECTED: * Betslip is closed
        """
        pass
