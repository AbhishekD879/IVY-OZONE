import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.betslip
@vtest
class Test_C3249962_No_Duplicate_Bets_on_Betslip_after_multiple_clicks(Common):
    """
    TR_ID: C3249962
    NAME: No Duplicate Bets on Betslip after multiple clicks
    DESCRIPTION: This test case verifies that user is not able to place duplicate bets by multiple clicking on Bet Now button
    PRECONDITIONS: User is logged in
    """
    keep_browser_open = True

    def test_001_add_selection_to_the_betslip_and_open_betslip(self):
        """
        DESCRIPTION: Add selection to the Betslip and open Betslip
        EXPECTED: 
        """
        pass

    def test_002_enter_stake(self):
        """
        DESCRIPTION: Enter Stake
        EXPECTED: 
        """
        pass

    def test_003_click_multiple_times_on_place_bet_button(self):
        """
        DESCRIPTION: Click multiple times on 'PLACE BET' button
        EXPECTED: *  Bet is placed only once
        EXPECTED: *  Bet Receipt is shown with one placed bet
        EXPECTED: *  Only one placebet request is present in network
        """
        pass

    def test_004_verify_users_balance(self):
        """
        DESCRIPTION: Verify User's balance
        EXPECTED: User's balance is decreased by entered Stake, not more than that
        """
        pass

    def test_005_verify_open_bets_page(self):
        """
        DESCRIPTION: Verify 'Open Bets' page
        EXPECTED: Only one placed bet is present on 'Open Bets' page, there are no duplicated bets
        """
        pass
