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
class Test_C883820_Verify_Quick_Bet_for_not_Logged_In(Common):
    """
    TR_ID: C883820
    NAME: Verify Quick Bet for not Logged In
    DESCRIPTION: This test case verifies Quick Bet for not Logged in
    PRECONDITIONS: Quick Bet functionality should be enabled in CMS and user`s settings
    PRECONDITIONS: Quick Bet functionality is available for Mobile ONLY
    PRECONDITIONS: User should be logged out
    PRECONDITIONS: For Step #8 and Step #10
    PRECONDITIONS: User should not have any popup windows appear after starting session
    PRECONDITIONS: For Step #11
    PRECONDITIONS: User should have one or more popup windows appear after starting session:
    PRECONDITIONS: Terms and Conditions
    PRECONDITIONS: Verify Your Account (Netverify)
    PRECONDITIONS: Deposit Limits
    PRECONDITIONS: Quick Deposit
    PRECONDITIONS: Free Bet
    PRECONDITIONS: Casino bonuses
    """
    keep_browser_open = True

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_add_sport_race_selection_to_quick_bet(self):
        """
        DESCRIPTION: Add <Sport>/ <Race> selection to Quick Bet
        EXPECTED: Quick Bet is displayed at the bottom of the page
        EXPECTED: Added selection and all data are displayed in Quick Bet
        """
        pass

    def test_003_verify_quick_bet_displaying(self):
        """
        DESCRIPTION: Verify Quick Bet displaying
        EXPECTED: Quick Bet consists of:
        EXPECTED: 'Quick Bet' header and 'X' icon
        EXPECTED: Added selection`s details
        EXPECTED: 'Odds' label and field
        EXPECTED: 'Stake' field
        EXPECTED: 'Each Way' label and checkbox (if available)
        EXPECTED: 'Quick Stakes' buttons
        EXPECTED: 'Stake' and 'Est. Returns' labels and corresponding values
        EXPECTED: 'ADD TO BETSLIP' and 'LOGIN & PLACE BET' button
        """
        pass

    def test_004_verify_login__place_bet_button(self):
        """
        DESCRIPTION: Verify 'LOGIN & PLACE BET' button
        EXPECTED: 'LOGIN & PLACE BET' button is disabled by default
        """
        pass

    def test_005_enter_valid_value_on_stake_field(self):
        """
        DESCRIPTION: Enter valid value on 'Stake' field
        EXPECTED: 'LOGIN & PLACE BET' button becomes enabled
        """
        pass

    def test_006_tap_on_login__place_bet_button(self):
        """
        DESCRIPTION: Tap on 'LOGIN & PLACE BET' button
        EXPECTED: An overlay Login window is displayed
        """
        pass

    def test_007_fill_valid_username__password_and_tap_on_login__place_bet_button(self):
        """
        DESCRIPTION: Fill valid username / password and tap on 'LOGIN & PLACE BET' button
        EXPECTED: User session is started and bet is placed according to selected <Sport>/ <Race>, 'Odds' and 'Stake'
        """
        pass

    def test_008_verify_the_bet_confirmation(self):
        """
        DESCRIPTION: Verify the Bet Confirmation
        EXPECTED: Same Selection and Market is displayed where the bet was placed;
        EXPECTED: Local Time (if available) and Event is displayed;
        EXPECTED: **Unique Bet ID is displayed;
        EXPECTED: The balance is correctly updated;
        EXPECTED: **Odds are exactly the same as when bet has been placed;
        EXPECTED: **Unit Stake is correctly displayed;
        EXPECTED: **Total Stake is correctly displayed;
        EXPECTED: **Estimated Returns is exactly the same as when bet has been placed;
        """
        pass

    def test_009_log_out_from_app(self):
        """
        DESCRIPTION: Log out from app
        EXPECTED: User is logged out
        """
        pass

    def test_010_repeat_steps_1_7log_in_with_user_that_has_lower_balance_than_the_amount_entered_on_stake_and_credit_card_added(self):
        """
        DESCRIPTION: Repeat steps #1-7
        DESCRIPTION: Log in with user that has lower balance than the amount entered on 'Stake' and credit card added
        EXPECTED: Quick bet appears at the bottom of the page and should display:
        EXPECTED: 'Please deposit a min of "<currency symbol>XX.XX" to continue placing your bet' where,
        EXPECTED: <currency symbol> - currency that was set during registration
        EXPECTED: 'XX.XX' - rest amount that is needed to place a bet
        """
        pass

    def test_011_repeat_steps_1_7log_in_with_an_user_that_has_an_expected_popup_window_to_appear_for_each_case_belowterms_and_conditionsverify_your_account_netverifydeposit_limitsquick_depositfree_betcasino_bonuses(self):
        """
        DESCRIPTION: Repeat Steps #1-7
        DESCRIPTION: Log in with an user that has an expected popup window to appear for each case below:
        DESCRIPTION: Terms and Conditions
        DESCRIPTION: Verify Your Account (Netverify)
        DESCRIPTION: Deposit Limits
        DESCRIPTION: Quick Deposit
        DESCRIPTION: Free Bet
        DESCRIPTION: Casino bonuses
        EXPECTED: Respective popup window should appear and bet is not placed
        """
        pass
