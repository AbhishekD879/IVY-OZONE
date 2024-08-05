import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.quick_bet
@vtest
class Test_C888567_Verify_Quick_Deposit_section_for_users_with_free_bets(Common):
    """
    TR_ID: C888567
    NAME: Verify Quick Deposit section for users with free bets
    DESCRIPTION: This test case verifies Quick Deposit section for users with free bets available
    PRECONDITIONS: 1. Quick Bet functionality should be enabled in CMS and user`s settings
    PRECONDITIONS: 2. Quick Bet functionality is available for Mobile ONLY
    PRECONDITIONS: 3. User is logged in, has 0 balance and free bets and at list one credit card added to his account
    PRECONDITIONS: 4. Users have the cards added to his account
    """
    keep_browser_open = True

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_add_selection_to_quick_bet(self):
        """
        DESCRIPTION: Add selection to Quick Bet
        EXPECTED: * Quick bet appears at the bottom of the page
        EXPECTED: * 'Use Free bet' link is displayed below event name
        """
        pass

    def test_003_click_use_free_bet_link_and_select_free_bet_from_the_pop_up(self):
        """
        DESCRIPTION: Click 'Use Free bet' link and select Free bet from the pop-up.
        EXPECTED: * Free bet is selected
        EXPECTED: * 'Please deposit a min of <currency symbol>XX.XX to continue placing your bet' message is NOT displayed
        EXPECTED: * Stake is equal to free bet value
        """
        pass

    def test_004_enter_value_in_stake_field_that_exceeds_users_balance(self):
        """
        DESCRIPTION: Enter value in 'Stake' field that exceeds user's balance
        EXPECTED: * Info icon and 'Please deposit a min of "<currency symbol>XX.XX to continue placing your bet' message is displayed below the on-screen keyboard immediately for **Ladbrokes** brand
        EXPECTED: * The same message(without icon) is displayed below 'QUICK BET' header for **Coral** brand
        EXPECTED: where,
        EXPECTED: <currency symbol> - currency that was set during registration
        EXPECTED: 'XX.XX' - difference between entered(into a field) stake value and users balance
        EXPECTED: * Total Stake is equal to free bet value + stake value
        """
        pass

    def test_005_log_out_of_app(self):
        """
        DESCRIPTION: Log out of app
        EXPECTED: User is logged out
        """
        pass

    def test_006_log_in_with_user_that_has_positive_balance_credit_cards_and_free_bets_added_to_his_account(self):
        """
        DESCRIPTION: Log in with user that has positive balance, credit cards and free bets added to his account
        EXPECTED: User is logged in
        """
        pass

    def test_007_repeat_steps_2_5(self):
        """
        DESCRIPTION: Repeat steps #2-5
        EXPECTED: 
        """
        pass
