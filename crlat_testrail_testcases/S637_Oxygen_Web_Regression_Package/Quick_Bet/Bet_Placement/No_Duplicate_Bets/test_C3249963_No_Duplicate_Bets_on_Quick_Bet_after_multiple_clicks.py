import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.quick_bet
@vtest
class Test_C3249963_No_Duplicate_Bets_on_Quick_Bet_after_multiple_clicks(Common):
    """
    TR_ID: C3249963
    NAME: No Duplicate Bets on Quick Bet after multiple clicks
    DESCRIPTION: This test case verifies that user is not able to place duplicate bets by multiple clicking on Bet Now button
    DESCRIPTION: AUTOTEST [C9697979]
    PRECONDITIONS: User is logged in
    """
    keep_browser_open = True

    def test_001_add_selection_to_quick_bet(self):
        """
        DESCRIPTION: Add selection to Quick Bet
        EXPECTED: 
        """
        pass

    def test_002_enter_stake(self):
        """
        DESCRIPTION: Enter Stake
        EXPECTED: 
        """
        pass

    def test_003_click_multiple_times_on_bet_now_button(self):
        """
        DESCRIPTION: Click multiple times on 'BET NOW' button
        EXPECTED: *  Bet is placed only once
        EXPECTED: *  Bet Receipt is shown with one placed bet
        EXPECTED: *  Only one request 30011 is present in remote betslip websocket
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
