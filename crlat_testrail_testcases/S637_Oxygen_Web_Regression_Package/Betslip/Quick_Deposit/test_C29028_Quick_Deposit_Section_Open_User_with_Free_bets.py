import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C29028_Quick_Deposit_Section_Open_User_with_Free_bets(Common):
    """
    TR_ID: C29028
    NAME: Quick Deposit Section Open User with Free bets
    DESCRIPTION: AUTOTEST: [C2507407]
    DESCRIPTION: This test case verifies 'Quick Deposit' section for user with free bets available
    PRECONDITIONS: 1.   User account with **0 balance, at least one registered Credit Card and Free Bets available** (Additional pop-up Quick Deposit)
    PRECONDITIONS: 2.   User account with **positive balance, at least one registered Credit Card ** **and Free Bets available**
    """
    keep_browser_open = True

    def test_001_load_application_and_log_in_with_account_1(self):
        """
        DESCRIPTION: Load application and Log in with account 1
        EXPECTED: - User is logged in
        """
        pass

    def test_002_add_any_selections_to_the_bet_slip_and_open_the_betlip_pagewidget(self):
        """
        DESCRIPTION: Add any selection(s) to the Bet Slip and Open the Betіlip page/widget
        EXPECTED: - Made selection(s) is displayed within Betіslip content area
        EXPECTED: - **OX 98**: 'Free Bet Available' dropdown is present, **from OX 99**: Use Freebet Link is displayed for selection
        EXPECTED: **Coral**
        EXPECTED: * 'QUICK DEPOSIT' section is displayed on the bottom of the Bet Slip
        EXPECTED: **Ladbrokes**
        EXPECTED: - There is NO 'Quick Deposit' section or error message displayed on the Bet Slip
        """
        pass

    def test_003_ox_98_go_tofree_bet_available_dropdown_from_ox_99_click_on_use_free_bet_link_and_select_one_of_available_free_bets(self):
        """
        DESCRIPTION: **OX 98**: Go to 'Free Bet Available' dropdown/ **from OX 99**: Click on Use Free Bet link and select one of available Free bets
        EXPECTED: - Free bet is chosen for selection(s)
        EXPECTED: - 'QUICK DEPOSIT' section in NOT shown (as 'Total Stake' = 'Free Bet Stake')
        """
        pass

    def test_004_enter_stake_for_the_added_selections_which_amount_exceeds_user_balance(self):
        """
        DESCRIPTION: Enter 'Stake' for the added selection(s) which amount exceeds user balance
        EXPECTED: - Quick Deposit section is displayed
        EXPECTED: - Value on 'Please deposit a min of <currency>XX.XX to continue placing your bet' default message is changed according to entered stake
        """
        pass

    def test_005_clear_bet_slip___log_out(self):
        """
        DESCRIPTION: Clear Bet Slip -> Log Out
        EXPECTED: - "You have no selections in the slip." message is shown at the top of Betslip content area
        EXPECTED: - User is logged out
        """
        pass

    def test_006_log_in_with_account_2(self):
        """
        DESCRIPTION: Log in with account 2
        EXPECTED: - User is logged in
        """
        pass

    def test_007_add_any_selections_to_the_bet_slip_and_open_the_bet_slip_pagewidget(self):
        """
        DESCRIPTION: Add any selection(s) to the Bet Slip and Open the Bet Slip page/widget
        EXPECTED: - Selection(s) is displayed within Bet Slip content area
        EXPECTED: - Use Free Bet link is present
        """
        pass

    def test_008_click_tap_on_use_free_bet_linkselect_one_of_available_free_bets_from_free_bet_available_drop_down(self):
        """
        DESCRIPTION: Click/ Tap on Use Free Bet link
        DESCRIPTION: Select one of available Free bets from 'Free Bet Available' drop down
        EXPECTED: - Free bet is chosen for selection(s)
        EXPECTED: - 'QUICK DEPOSIT' section in NOT displayed (as 'Total Stake' = 'Free Bet Stake')
        """
        pass

    def test_009_enter_stake_for_the_added_selections_which_amount_exceeds_user_balance(self):
        """
        DESCRIPTION: Enter 'Stake' for the added selection(s) which amount exceeds user balance
        EXPECTED: * 'Please deposit a min of "<currency symbol>XX.XX to continue placing your bet' error message is displayed at the bottom of Betslip immediately
        EXPECTED: where,
        EXPECTED: <currency symbol> - currency that was set during registration
        EXPECTED: 'XX.XX' - the difference between entered stake value and users balance
        EXPECTED: * 'PLACE BET' button becomes 'MAKE A DEPOSIT' immediately and is enabled by default
        """
        pass

    def test_010_clicktap_make_a_deposit_button(self):
        """
        DESCRIPTION: Click/Tap 'MAKE A DEPOSIT' button
        EXPECTED: - Quick Deposit section is displayed
        """
        pass
