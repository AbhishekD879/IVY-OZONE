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
class Test_C2507410_Verify_Log_In_Bet_for_the_User_with_Insufficient_Balance(Common):
    """
    TR_ID: C2507410
    NAME: Verify 'Log In & Bet' for the User with Insufficient Balance
    DESCRIPTION: This test case verifies 'Log In & Bet' button for the User with Insufficient Balance
    PRECONDITIONS: Make sure you have user account with:
    PRECONDITIONS: Added (also Active) credit card(s) and insufficient balance to place a desired bet
    """
    keep_browser_open = True

    def test_001_add_1_selection_to_the_betslip(self):
        """
        DESCRIPTION: Add 1 selection to the Betslip
        EXPECTED: 
        """
        pass

    def test_002_open_betslip(self):
        """
        DESCRIPTION: Open Betslip
        EXPECTED: 1. Betslip is opened
        EXPECTED: 2. Added single selection is present
        EXPECTED: 3. 'LOGIN & PLACE BET'/'LOGIN AND PLACE BET' button is disabled
        """
        pass

    def test_003_enter_a_stake_for_the_selection_that_will_surely_exceed_users_balance_once_you_log_inby_5_for_gbp_usd_eur__50_kr(self):
        """
        DESCRIPTION: Enter a stake for the selection, that will surely exceed user's balance, once you log in(by 5 for GBP, USD, EUR / 50 KR)
        EXPECTED: 'LOGIN & PLACE BET'/'LOGIN AND PLACE BET' button becomes enabled
        """
        pass

    def test_004_tap_on_login__place_betlogin_and_place_bet_button(self):
        """
        DESCRIPTION: Tap on 'LOGIN & PLACE BET'/'LOGIN AND PLACE BET' button
        EXPECTED: 'LOG IN' pop-up is opened
        """
        pass

    def test_005_log_in_with_user_from_pre_conditions(self):
        """
        DESCRIPTION: Log In with user from pre-conditions
        EXPECTED: 1. Betslip is NOT refreshed
        EXPECTED: 2. Bet is NOT placed automatically
        EXPECTED: 3. Funds value = Stake - Balance
        EXPECTED: 4.  'LOGIN & PLACE BET'/'LOGIN AND PLACE BET' button label is changed to 'MAKE A DEPOSIT'
        EXPECTED: 5. 'MAKE A DEPOSIT' button is enabled
        """
        pass

    def test_006_tap_on_make_a_deposit_button(self):
        """
        DESCRIPTION: Tap on 'MAKE A DEPOSIT' button
        EXPECTED: 1. 'Quick Deposit' section is expanded
        EXPECTED: 2. 'MAKE A DEPOSIT' button label is changed 'DEPOSIT & PLACE BET'
        EXPECTED: 3. 'DEPOSIT & PLACE BET' button is disabled
        EXPECTED: 4. Funds needed for bet: <currency symbol>XX.XX** message is displayed on the red background, it is anchored to the footer of the Betslip
        """
        pass

    def test_007_clear_stake_field_within_betslip_for_the_added_selection(self):
        """
        DESCRIPTION: Clear 'Stake' field within Betslip for the added selection
        EXPECTED: 1. 'Quick Deposit' section disappears
        EXPECTED: 2. Button states 'PLACE BET'
        EXPECTED: 3. 'PLACE BET' button is disabled
        """
        pass

    def test_008_place_a_bet_that_will_make_your_users_balance_000(self):
        """
        DESCRIPTION: Place a bet that will make your user's balance '0.00'
        EXPECTED: Bet is successfully placed
        EXPECTED: Bet receipt is shown
        """
        pass

    def test_009_tap_reuse_selections_button_shown_in_betslip(self):
        """
        DESCRIPTION: Tap 'REUSE SELECTIONS' button shown in Betslip
        EXPECTED: Betslip is reopened
        EXPECTED: 'Quick Deposit' section is expanded
        EXPECTED: Button states 'DEPOSIT & PLACE BET'
        EXPECTED: 'DEPOSIT & PLACE BET' button is disabled
        EXPECTED: https://jira.egalacoral.com/browse/BMA-50509 closed by business
        """
        pass

    def test_010_clear_betslip_log_out_and_repeat_steps_1_5_with_the_same_userthat_now_has_000_balance(self):
        """
        DESCRIPTION: Clear Betslip, Log Out and repeat steps 1-5 with the same user(that now has '0.00' Balance)
        EXPECTED: Expected Results for steps 1-4 should match
        EXPECTED: Expected Result for the repeated Step 5 executions is:
        EXPECTED: * Betslip is reopened
        EXPECTED: * 'Quick Deposit' section is expanded
        EXPECTED: * Button states 'DEPOSIT & PLACE BET'
        EXPECTED: * 'DEPOSIT & PLACE BET' button is disabled
        """
        pass
