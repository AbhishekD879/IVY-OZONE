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
class Test_C16627546_Vanilla_Place_a_Bet_when_entering_invalid_credentials_for_Login(Common):
    """
    TR_ID: C16627546
    NAME: [Vanilla] Place a Bet when entering invalid credentials for Login
    DESCRIPTION: This test case verifies Bet Placement when entering invalid credentials for Login.
    PRECONDITIONS: Make sure that user is logged out.
    PRECONDITIONS: For <Sport> it is possible to place a bet from:
    PRECONDITIONS: event landing page
    PRECONDITIONS: event details page
    PRECONDITIONS: For <Races> it is possible to place a bet from:
    PRECONDITIONS: 'Next 4' module
    PRECONDITIONS: event details page
    PRECONDITIONS: Extra Info:
    PRECONDITIONS: Bet placement process will be automatically started JUST after session token will be set for user.
    PRECONDITIONS: Behavior of pop-ups is not changed by this functionality e.g. if 'Terms and Conditions' pop-up appears - user will need to accept new terms to be able to place bets.
    """
    keep_browser_open = True

    def test_001_open_application(self):
        """
        DESCRIPTION: Open application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_add_any_market_for_betting(self):
        """
        DESCRIPTION: Add any market for betting
        EXPECTED: Quick Bet is opened:
        EXPECTED: * 'ADD TO BETSLIP' is active
        EXPECTED: * 'LOGIN & PLACE BET' button is not active
        """
        pass

    def test_003_enter_at_least_one_stake_for_any_selection(self):
        """
        DESCRIPTION: Enter at least one stake for any selection
        EXPECTED: Stake is entered and displayed correctly
        EXPECTED: * 'ADD TO BETSLIP' is active
        EXPECTED: * 'LOGIN & PLACE BET' button is active
        """
        pass

    def test_004_tap_on_login__place_bet_button(self):
        """
        DESCRIPTION: Tap on 'LOGIN & PLACE BET' button
        EXPECTED: * Logged out user is not able to place a bet
        EXPECTED: * 'Log In' pop-up opens
        EXPECTED: * Username and Password fields are available
        """
        pass

    def test_005_enter_invalid_credentials_of_users_account___tap_on_log_in_button(self):
        """
        DESCRIPTION: Enter *invalid* credentials of user's account -> Tap on 'LOG IN' button
        EXPECTED: There is error message: 'The credentials entered are incorrect'
        """
        pass

    def test_006_enter_valid_credentials_of_users_account_for_which_balance_is_positive__tap_log_in(self):
        """
        DESCRIPTION: Enter valid credentials of user's account for which balance is positive
        DESCRIPTION: -> Tap 'LOG IN'
        EXPECTED: * User is logged in
        EXPECTED: * User can't do any modification for bet that is ongoing
        EXPECTED: * Bets are placed successfully (NOTE: if at least one pop-up is expected after login, Bet is NOT placed automatically)
        EXPECTED: * Bet Receipt appears after successful bet placement
        """
        pass

    def test_007_repeat_steps_1__4(self):
        """
        DESCRIPTION: Repeat steps 1- 4
        EXPECTED: 
        """
        pass

    def test_008_enter_valid_credentials_of_users_account_for_which_balance_is_positive_and_at_least_one_pop_up_is_expected_after_login_freebet_odds_boost_are_available_for_a_user_or_tutorial_overlay_if_cash_was_cleared__tap_log_in_button(self):
        """
        DESCRIPTION: Enter valid credentials of user's account for which balance is positive and at least one pop-up is expected after login (freebet, odds boost are available for a user) or tutorial overlay (if cash was cleared))-> Tap 'LOG IN' button
        EXPECTED: * User is logged in and expected pop-ups appear
        EXPECTED: * Quickbet is NOT closed
        EXPECTED: * Bet is NOT placed automatically
        EXPECTED: * After user will deal with pop-ups then *'Place Bet' button* will be enabled within Betslip
        """
        pass

    def test_009_tap_on_place_bet_button(self):
        """
        DESCRIPTION: Tap on 'Place Bet' button
        EXPECTED: Bet is placed successfully as for logged in user
        """
        pass
