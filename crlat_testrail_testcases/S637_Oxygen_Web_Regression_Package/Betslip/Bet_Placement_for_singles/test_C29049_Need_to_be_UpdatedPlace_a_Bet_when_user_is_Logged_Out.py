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
class Test_C29049_Need_to_be_UpdatedPlace_a_Bet_when_user_is_Logged_Out(Common):
    """
    TR_ID: C29049
    NAME: [Need to be Updated]Place a Bet when user is Logged Out
    DESCRIPTION: This test case verifies bet placement when user is Logged Out
    DESCRIPTION: **TO UPDATE**
    DESCRIPTION: Step 6, 10 - 2  Betslip is NOT refreshed . (Actually it refreshed)
    PRECONDITIONS: Make sure that user is logged out.
    PRECONDITIONS: For <Sport> it is possible to place a bet from:
    PRECONDITIONS: - event landing page
    PRECONDITIONS: - event details page
    PRECONDITIONS: For <Races> it is possible to place a bet from:
    PRECONDITIONS: - 'Next 4' module
    PRECONDITIONS: - event details page
    PRECONDITIONS: **Extra Info:**
    PRECONDITIONS: *   Bet placement process will be automatically started JUST after session token will be set for the user.
    PRECONDITIONS: *   Behavior of pop-ups is not changed by this functionality e.g. if 'Terms and Conditions' pop-up appears - user will need to accept new terms to be able to place bets.
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_add_selections_to_the_betslip(self):
        """
        DESCRIPTION: Add selections to the Betslip
        EXPECTED: Betslip counter is increased
        """
        pass

    def test_003_go_to_the_betslip_singles_section(self):
        """
        DESCRIPTION: Go to the Betslip->'Singles' section
        EXPECTED: 1.  Betslip is opened
        EXPECTED: 2.  Added single selections are present
        EXPECTED: 3. 'Log in & Place Bet' button is disabled
        """
        pass

    def test_004_enter_at_least_one_stake_for_any_selection(self):
        """
        DESCRIPTION: Enter at least one stake for any selection
        EXPECTED: 1. Stake is entered and displayed correctly
        EXPECTED: 2. 'Log in & Place Bet' button becomes enabled
        """
        pass

    def test_005_tap_log_in__place_bet_button(self):
        """
        DESCRIPTION: Tap 'Log in & Place Bet' button
        EXPECTED: 1.  Logged out user is not able to place a bet
        EXPECTED: 2.  'Log In' pop-up opens
        EXPECTED: 3.  Username and Password fields are available
        EXPECTED: 4.  **"Log in"** button is active by default
        """
        pass

    def test_006_enter_valid_credentials_of_users_account_for_which_balance_is_positive_and_at_least_one_pop_up_is_expected_after_login___tap_log_in_button(self):
        """
        DESCRIPTION: Enter valid credentials of user's account for which balance is positive and **at least one** pop-up is expected after login -> Tap 'Log in' button
        EXPECTED: 1.  User is logged in and expected pop-ups appear
        EXPECTED: 2.  Betslip is NOT refreshed
        EXPECTED: 3.  Bet is NOT placed automatically
        EXPECTED: 4.  After user will deal with pop-ups then** 'Bet Now' button** will be enabled within Betslip
        """
        pass

    def test_007_tap_place_bet_button(self):
        """
        DESCRIPTION: Tap 'Place Bet' button
        EXPECTED: Bet is placed successfully as for logged in user
        """
        pass

    def test_008_log_out_from_the_application(self):
        """
        DESCRIPTION: Log out from the application
        EXPECTED: User is logged out successfully
        """
        pass

    def test_009_repeat_steps_1_5(self):
        """
        DESCRIPTION: Repeat steps #1-5
        EXPECTED: 
        """
        pass

    def test_010_enter_valid_credentials_of_users_account_for_which_balance_is_positive_and_no_pop_ups_are_expected_after_login___tap_log_in(self):
        """
        DESCRIPTION: Enter valid credentials of user's account for which balance is positive and **NO **pop-ups are expected after login -> Tap 'Log in'
        EXPECTED: 1.  User is logged in
        EXPECTED: 2.  Betslip is NOT refreshed
        EXPECTED: 3.  Bets are placed successfully
        EXPECTED: 4.  Bet Receipt is displayed
        """
        pass

    def test_011_log_out_from_the_application(self):
        """
        DESCRIPTION: Log out from the application
        EXPECTED: User is logged out successfully
        """
        pass

    def test_012_repeat_steps_1_5(self):
        """
        DESCRIPTION: Repeat steps #1-5
        EXPECTED: 
        """
        pass

    def test_013_enter_valid_credentials_of_users_account_for_which_balance_is_positive_andnopop_ups_are_expected_after_login__tap_log_in_and_right_after_that_trigger_error_occurance_eg_suspension_price_change(self):
        """
        DESCRIPTION: Enter valid credentials of user's account for which balance is positive and **NO **pop-ups are expected after login ->Tap 'Log in' and right after that trigger error occurance (e.g. suspension, price change)
        EXPECTED: 1.  Bet placement process starts automatically after login, hovewer it is interrupted by corresponding message about error
        EXPECTED: 2.  Betslip is NOT refreshed
        EXPECTED: 3.  Bet is not placed
        EXPECTED: 4.  User needs to make changes in the Betslip to be able to place a bet
        EXPECTED: 5.  After user will deal with error then** 'Bet Now' button** will be anabled within Betslip
        """
        pass

    def test_014_tap_place_bet_button(self):
        """
        DESCRIPTION: Tap 'Place Bet' button
        EXPECTED: Bet is placed successfully as for logged in user
        """
        pass

    def test_015_log_out_from_the_application(self):
        """
        DESCRIPTION: Log out from the application
        EXPECTED: User is logged out successfully
        """
        pass

    def test_016_add_several_selections_from_different_events_to_the_betslip(self):
        """
        DESCRIPTION: Add several selections from different events to the Betslip
        EXPECTED: Betslip counter is increased
        """
        pass

    def test_017_go_to_the_betslip___multiples_section(self):
        """
        DESCRIPTION: Go to the Betslip -> 'Multiples' section
        EXPECTED: 1.  Betslip is opened
        EXPECTED: 2.  Added multiple selections are present
        """
        pass

    def test_018_repeat_steps_4_15(self):
        """
        DESCRIPTION: Repeat steps #4-15
        EXPECTED: 
        """
        pass
