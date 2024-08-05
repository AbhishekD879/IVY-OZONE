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
class Test_C15744052_Verify_International_Tote_Exacta_Bet_Receipt(Common):
    """
    TR_ID: C15744052
    NAME: Verify International Tote Exacta Bet Receipt
    DESCRIPTION: This test case verifies International Exacta bet receipt, which appears in betslip after the user has placed an Exacta Tote bet
    DESCRIPTION: Please note that we are NOT ALLOWED to Place a Tote bets on HL and PROD environments!
    PRECONDITIONS: The User's account balance is sufficient to cover the bet stake
    PRECONDITIONS: User is logged in
    PRECONDITIONS: International Tote feature is enabled in CMS
    PRECONDITIONS: Win pool type is available for International HR Event
    PRECONDITIONS: User should have placed an International Exacta Tote bet
    """
    keep_browser_open = True

    def test_001_verify_exacta_international_tote_bet_receipt_header(self):
        """
        DESCRIPTION: Verify Exacta International Tote Bet Receipt Header
        EXPECTED: Bet Receipt header contains the following elements:
        EXPECTED: 'X' button
        EXPECTED: 'Bet Receipt' title
        EXPECTED: 'User Balance' button
        """
        pass

    def test_002_verify_exacta_international_tote_bet_receipt_subheader(self):
        """
        DESCRIPTION: Verify Exacta International Tote Bet Receipt subheader
        EXPECTED: Bet Receipt subheader contains the following elements:
        EXPECTED: 'Check' icon and 'Bet Placed Successfully' text
        EXPECTED: Date and time in the next format: i.e. 19/09/2019, 14:57 and aligned by the right side
        EXPECTED: Bet count in the next format: 'Your Bets:(X)' where 'X' is the number of bets placed in for that receipt
        """
        pass

    def test_003_verify_exacta_international_tote_bet_receipt_card_for_exacta_bet(self):
        """
        DESCRIPTION: Verify Exacta International Tote Bet Receipt card for Exacta Bet
        EXPECTED: The following information is displayed on the bet receipt:
        EXPECTED: Bet type name ("Singles " label in the section header)
        EXPECTED: Bet ID(Coral)/Receipt No(Ladbrokes)
        EXPECTED: Tote selections name
        EXPECTED: Eg: 1st Drops of Jup
        EXPECTED: 2nd Massina
        EXPECTED: Bet Type name / Meeting ( Exacta / 13.25 Place )
        EXPECTED: For Coral: Total Stake: /Esti Returns: N/A Layout
        EXPECTED: Total Stake /Estimate Returns =N/A Layout
        EXPECTED: For Ladbrokes: Stake on this Bet: Potential Returns: N/A Layout
        EXPECTED: Total Stake /Potential Returns =N/A Layout
        """
        pass

    def test_004_verify_bet_id(self):
        """
        DESCRIPTION: Verify Bet ID
        EXPECTED: Bet ID corresponds to the value, received from OpenBet
        """
        pass

    def test_005_verify_unit_stake(self):
        """
        DESCRIPTION: Verify Unit Stake
        EXPECTED: The unit Stake value is the same as the user has entered during bet placement
        """
        pass

    def test_006_verify_est_returnspotential_returns(self):
        """
        DESCRIPTION: Verify Est. Returns/Potential returns
        EXPECTED: Est. Returns/Potential value is "N/A"
        """
        pass

    def test_007_verify_total_stake_and_estpotential_returns_at_the_bottom_of_the_betslip(self):
        """
        DESCRIPTION: Verify Total Stake and Est./Potential Returns at the bottom of the betslip
        EXPECTED: Total Stake value corresponds to the actual total stake based on the stake value entered
        EXPECTED: Est./Potential Returns value is "N/A"
        """
        pass

    def test_008_click_on_reuse_selection_button(self):
        """
        DESCRIPTION: Click on 'Reuse Selection' button
        EXPECTED: "Exacta" bet appears in the BetSlip again
        """
        pass

    def test_009_place_an_international_tote_exacta_bet_again(self):
        """
        DESCRIPTION: Place an International Tote Exacta bet again
        EXPECTED: Exacta bet is placed successfully
        EXPECTED: Bet Receipt appears
        """
        pass
