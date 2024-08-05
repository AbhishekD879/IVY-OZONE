import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.sports
@vtest
class Test_C28582_Bet_Placement_on_Football_Jackpot_pool_when_user_is_Logged_Out(Common):
    """
    TR_ID: C28582
    NAME: Bet Placement on Football 'Jackpot' pool when user is Logged Out
    DESCRIPTION: This test case verifies Bet Placement on Football 'Jackpot' pool when user is Logged Out
    DESCRIPTION: **Jira ticket:** BMA-5359 (Betslip Login - Login and Place Bet)
    PRECONDITIONS: *   Football 'Jackpot' pool is available
    PRECONDITIONS: *   User is logged out
    PRECONDITIONS: Note:
    PRECONDITIONS: Line - 15 selections, 1 from each event
    PRECONDITIONS: Total Lines - number of selected combinations of 15 match results
    PRECONDITIONS: **Extra Info:**
    PRECONDITIONS: *   Bet placement process will be automatically started JUST after session token will be set for user
    PRECONDITIONS: *   Behavior of pop-ups is not changed by this functionality e.g. if 'Terms and Conditions' pop-up appears - user needs to accept new terms to be able to place bets
    PRECONDITIONS: *   Behavior is not changed by this functionality in case of errors
    """
    keep_browser_open = True

    def test_001_load_invictus_application(self):
        """
        DESCRIPTION: Load Invictus application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_tapfootball_icon_on_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap 'Football' icon on the Sports Menu Ribbon
        EXPECTED: **Desktop**:
        EXPECTED: * <Sport> Landing Page is opened
        EXPECTED: * 'Matches'->'Today' sub tab is opened by default
        EXPECTED: **Mobile**:
        EXPECTED: * <Sport> Landing Page is opened
        EXPECTED: * 'Matches' tab is opened by default
        """
        pass

    def test_003_tap_jackpot_tab(self):
        """
        DESCRIPTION: Tap 'Jackpot' tab
        EXPECTED: 1.  Football 'Jackpot' tab is opened with 15 events available
        EXPECTED: 2.  Each event has 3 buttons
        """
        pass

    def test_004_make_at_least_15_selection_at_least_1_from_each_event_using_lucky_dip_option_or_manually(self):
        """
        DESCRIPTION: Make at least 15 selection (at least 1 from each event) using 'Lucky Dip' option or manually
        EXPECTED: 1.  Selections that were made are highlighted
        EXPECTED: 2.  'Bet Now' button is enabled
        """
        pass

    def test_005_choose_stake_per_line_amount_and_tap_bet_now_button(self):
        """
        DESCRIPTION: Choose 'Stake Per Line' amount and tap 'Bet Now' button
        EXPECTED: 1.  Logged out user is not able to place a bet
        EXPECTED: 2.  'Log In' pop-up opens
        EXPECTED: 3.  Username and Password fields are available
        EXPECTED: 4.  **"Log In and Place Bet"** button is disabled by default
        """
        pass

    def test_006_enter_valid_credentials_of_users_account_for_which_balance_is_positive_and_at_least_one_pop_up_is_expected_after_login___tap_log_in_and_place_bet(self):
        """
        DESCRIPTION: Enter valid credentials of user's account for which balance is positive and **at least one** pop-up is expected after login -> Tap 'Log In and Place Bet'
        EXPECTED: 1.  User is logged in and expected pop-ups appear
        EXPECTED: 2.  Bet is NOT placed automatically
        EXPECTED: 3.  After user will deal with pop-ups then** 'Bet Now' button** will be anabled within Betslip
        """
        pass

    def test_007_tap_bet_now_button(self):
        """
        DESCRIPTION: Tap 'Bet Now' button
        EXPECTED: Pool bet is placed successfully as for logged in user
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

    def test_010_enter_valid_credentials_of_users_account_for_which_balance_is_positive_and_no_pop_ups_are_expected_after_login___tap_log_in_and_place_bet(self):
        """
        DESCRIPTION: Enter valid credentials of user's account for which balance is positive and **NO **pop-ups are expected after login -> Tap 'Log In and Place Bet'
        EXPECTED: 1.  User is logged in
        EXPECTED: 2.  Bet is placed successfully
        EXPECTED: 3.  User is redirected to Bet Receipt page
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

    def test_013_enter_valid_credentials_of_users_account_for_which_balance_is_not_enough_to_place_bet_andnopop_ups_are_expected_after_login___tap_log_in_and_place_bet(self):
        """
        DESCRIPTION: Enter valid credentials of user's account for which **balance is NOT enough to place bet** and **NO pop-ups are expected** after login -> Tap 'Log In and Place Bet'
        EXPECTED: 1.  Bet placement process starts automatically after login, hovewer it is interrupted by corresponding message about insufficient funds
        EXPECTED: 2.  Bet is not placed
        EXPECTED: 3.  User needs to deposit or change stake amount to be able to place a bet
        """
        pass

    def test_014_make_sure_balance_can_cover_the_selected_stake___tap_bet_now(self):
        """
        DESCRIPTION: Make sure balance can cover the selected stake -> Tap 'Bet Now'
        EXPECTED: Pool bet is placed successfully as for logged in user
        """
        pass

    def test_015_log_out_from_the_application(self):
        """
        DESCRIPTION: Log out from the application
        EXPECTED: 
        """
        pass

    def test_016_repeat_steps_1_5(self):
        """
        DESCRIPTION: Repeat steps #1-5
        EXPECTED: 
        """
        pass

    def test_017_enter_valid_credentials_of_users_account_for_which_balance_is_enough_to_place_bet_and_no_pop_ups_are_expected_after_login___tap_log_in_and_place_bet_in_case_whenbet_placement_on_displayed_pool_will_be_canceled_by_provider_or_services_will_not_respond(self):
        """
        DESCRIPTION: Enter valid credentials of user's account for which balance is enough to place bet and **NO **pop-ups are expected after login -> Tap 'Log In and Place Bet' in case when **bet placement on displayed pool will be canceled by provider or services will not respond**
        EXPECTED: 1.  Bet placement process starts automatically after login, hovewer it is interrupted by corresponding message about error
        EXPECTED: 2.  Bet is not placed
        """
        pass

    def test_018_make_at_least_15_selection_at_least_1_from_each_event_using_lucky_dip_option_or_manually(self):
        """
        DESCRIPTION: Make at least 15 selection (at least 1 from each event) using 'Lucky Dip' option or manually
        EXPECTED: 1.  Selections that were made are highlighted
        EXPECTED: 2.  'Bet Now' button is enabled
        """
        pass
