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
class Test_C15392881_Vanilla_Logged_out_user_Place_a_bet_on_Quickbet_for_logged_out_user(Common):
    """
    TR_ID: C15392881
    NAME: [Vanilla] [Logged out  user] Place a bet on Quickbet for logged out user
    DESCRIPTION: Verify that logged out user is able to place bet from Quickbet
    DESCRIPTION: NEED TO UPDATE!!!!
    DESCRIPTION: bet will not be placed automatically when there are pop-ups after login
    PRECONDITIONS: *Quickbet should be enabled in CMS
    PRECONDITIONS: *Make sure that that user is logged out
    """
    keep_browser_open = True

    def test_001_open_vanilla(self):
        """
        DESCRIPTION: Open Vanilla
        EXPECTED: The application is successfully loaded
        """
        pass

    def test_002_go_to_any_sport_eg_football___select_any_odd(self):
        """
        DESCRIPTION: Go to any Sport (e.g Football)--> Select any odd
        EXPECTED: Quick Bet appears in the bottom of the screen
        EXPECTED: "Login & Place Bet" button is disabled by default
        """
        pass

    def test_003_specify_any_quickstake_eg_5_(self):
        """
        DESCRIPTION: Specify any QuickStake (e.g. 5 )
        EXPECTED: "Login & Place Bet" button becomes enabled
        """
        pass

    def test_004_click_on_login__place_bet_button(self):
        """
        DESCRIPTION: Click on "Login & Place Bet" button
        EXPECTED: 'Log In' pop-up opens
        EXPECTED: Username and Password fields are available
        """
        pass

    def test_005_enter_valid_credentials_of_users_account_for_which_balance_is_positive____tap_log_in_button(self):
        """
        DESCRIPTION: Enter valid credentials of user's account for which balance is positive  -> Tap 'Log in' button
        EXPECTED: Bet is placed automatically
        EXPECTED: Bet Receipt with all betting details appears
        """
        pass

    def test_006_click_on_close_button(self):
        """
        DESCRIPTION: Click on "Close" button
        EXPECTED: Quick Bet is closed
        """
        pass

    def test_007_open_my_bets(self):
        """
        DESCRIPTION: Open "My Bets"
        EXPECTED: Just placed bet is displayed in Open Bets
        """
        pass
