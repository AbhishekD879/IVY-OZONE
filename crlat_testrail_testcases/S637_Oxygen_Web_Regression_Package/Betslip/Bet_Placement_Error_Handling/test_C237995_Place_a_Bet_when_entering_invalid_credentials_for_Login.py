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
class Test_C237995_Place_a_Bet_when_entering_invalid_credentials_for_Login(Common):
    """
    TR_ID: C237995
    NAME: Place a Bet when entering invalid credentials for Login
    DESCRIPTION: This test case verifies Bet Placement when entering invalid credentials for Login.
    PRECONDITIONS: Make sure that user is logged out.
    PRECONDITIONS: For <Sport> it is possible to place a bet from:
    PRECONDITIONS: event landing page
    PRECONDITIONS: event details page
    PRECONDITIONS: For <Races> it is possible to place a bet from:
    PRECONDITIONS: 'Next 4' module
    PRECONDITIONS: event details page
    PRECONDITIONS: *Extra Info:*
    PRECONDITIONS: Bet placement process will be automatically started JUST after session token will be set for user.
    PRECONDITIONS: Behavior of pop-ups is not changed by this functionality e.g. if 'Terms and Conditions' pop-up appears - user will need to accept new terms to be able to place bets.
    """
    keep_browser_open = True

    def test_001_add_selections_to_the_betslip(self):
        """
        DESCRIPTION: Add selections to the Betslip
        EXPECTED: Betslip counter is increased
        """
        pass

    def test_002_enter_at_least_one_stake_for_any_selection(self):
        """
        DESCRIPTION: Enter at least one stake for any selection
        EXPECTED: Stake is entered and displayed correctly
        """
        pass

    def test_003_tap_on_log_in__place_bet_button(self):
        """
        DESCRIPTION: Tap on 'Log in & Place Bet' button
        EXPECTED: * Logged out user is not able to place a bet
        EXPECTED: * 'Log In' pop-up opens
        EXPECTED: * Username and Password fields are available
        EXPECTED: * "Log In & Place Bet" button is disabled by default
        """
        pass

    def test_004_enter_invalid_credentials_of_users_account___tap_on_log_in__place_bet_button(self):
        """
        DESCRIPTION: Enter *invalid* credentials of user's account -> Tap on 'Log In & Place Bet' button
        EXPECTED: * Error message is displayed on 'Log In' pop-up
        EXPECTED: * User is NOT logged in and 'Log In' pop-up is still displaying
        EXPECTED: * Betslip is NOT closed
        EXPECTED: * Bet is NOT placed
        """
        pass

    def test_005_enter_valid_credentials_of_users_account_for_which_balance_is_positive_and_nopop_ups_are_expected_after_login_freebet_odds_boost_are_available_for_a_user_or_tutorial_overlay_if_cash_was_cleared___tap_log_in__place_bet(self):
        """
        DESCRIPTION: Enter valid credentials of user's account for which balance is positive and *NO*pop-ups are expected after login (freebet, odds boost are available for a user) or tutorial overlay (if cash was cleared)) -> Tap 'Log In & Place Bet'
        EXPECTED: * User is logged in
        EXPECTED: * Betslip is NOT closed
        EXPECTED: * Bets are placed successfully
        EXPECTED: * Bet Receipt page appears after successful bet placement
        """
        pass

    def test_006_repeat_steps_1__3(self):
        """
        DESCRIPTION: Repeat steps 1- 3
        EXPECTED: 
        """
        pass

    def test_007_enter_valid_credentials_of_users_account_for_which_balance_is_positive_and_at_least_one_pop_up_is_expected_after_login_freebet_odds_boost_are_available_for_a_user_or_tutorial_overlay_if_cash_was_cleared___tap_log_in__place_bet_button(self):
        """
        DESCRIPTION: Enter valid credentials of user's account for which balance is positive and at least one pop-up is expected after login (freebet, odds boost are available for a user) or tutorial overlay (if cash was cleared)) -> Tap 'Log In & Place Bet' button
        EXPECTED: * User is logged in and expected pop-ups appear
        EXPECTED: * Betslip is NOT closed
        EXPECTED: * Bet is NOT placed automatically
        EXPECTED: * After user will deal with pop-ups then *'Bet Now' button* will be enabled within Betslip
        """
        pass

    def test_008_tap_on_bet_now_button(self):
        """
        DESCRIPTION: Tap on 'Bet Now' button
        EXPECTED: Bet is placed successfully as for logged in user
        """
        pass
