import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.betslip
@vtest
class Test_C28122_Cash_Out_tab_With_Finished_Session(Common):
    """
    TR_ID: C28122
    NAME: 'Cash Out' tab With Finished Session
    DESCRIPTION: This test case verifies 'Cash Out' tab when user is logged out by server automatically when his/her session is over on the server.
    DESCRIPTION: **Jira tickets: **
    DESCRIPTION: *   BMA-7831 RIGHT COLUMN: Display Betslip
    DESCRIPTION: *   BMA-7845 RIGHT COLUMN: Include decoupled my Cashout tab
    DESCRIPTION: *   BMA-8173 DESKTOP GLOBAL RIGHT COLUMN
    PRECONDITIONS: To trigger event when session is over on the server please perform the following steps:
    PRECONDITIONS: *   Login to Invictus in one browser tab, go to 'Betslip' widget -> 'Cash Out' tab
    PRECONDITIONS: *   Login to Invictus in second browser tab, logout -> session is over on the server
    PRECONDITIONS: *   Navigate back to the first browser tab where user is still logged in, however there is no active session already
    """
    keep_browser_open = True

    def test_001_load_invictus_application_on_desktoptablet_device(self):
        """
        DESCRIPTION: Load Invictus application on desktop/tablet device
        EXPECTED: - Homepage is opened
        """
        pass

    def test_002_log_in_with_user_account_with_positive_balance(self):
        """
        DESCRIPTION: Log in with User account with positive balance
        EXPECTED: - User is Logged In
        """
        pass

    def test_003_placed_a_bet_on_pre_match_or_in_play_match_singles_and_multiple_betswhere_cash_out_and_partial_cash_out_offers_are_available_on_ss_see_cashoutavaily_on_event_and_market_levelto_besure_whether_comb_option_is_available(self):
        """
        DESCRIPTION: Placed a bet on Pre Match or In-Play match (Singles and Multiple bets) where Cash Out and Partial Cash Out offers are available (on SS see cashoutAvail="Y" on Event and Market level to be sure whether COMB option is available)
        EXPECTED: - Bet is placed
        EXPECTED: - User`s balance is decreased by value entered in 'Stake' field
        EXPECTED: - Bet Receipt is present with 'REUSE SELECTION' and 'DONE' buttons
        """
        pass

    def test_004_tap_done_button_and_navigate_to_cash_out_tab(self):
        """
        DESCRIPTION: Tap 'DONE' button and navigate to 'Cash Out' tab
        EXPECTED: - List of available  not  resulted bets is present
        """
        pass

    def test_005_make_steps_from_preconditions_to_finish_user_session(self):
        """
        DESCRIPTION: Make steps from preconditions to finish user session
        EXPECTED: 
        """
        pass

    def test_006_tap_cash_out_currency_xxx_button(self):
        """
        DESCRIPTION: Tap 'CASH OUT: <currency> X>XX' button
        EXPECTED: -   Popup message about logging out appears
        EXPECTED: -   User is logged out from the application and redirected to the Homepage
        EXPECTED: -   User is not able to see Cash Out bet lines and to perform Cash Out operations
        EXPECTED: -   'Please log in to see your Cash Out bets.' message and 'Log In' button are shown
        """
        pass

    def test_007_repeat_steps_2_5(self):
        """
        DESCRIPTION: Repeat steps #2-5
        EXPECTED: 
        """
        pass

    def test_008_try_to_move_slider_or_collapseexpand__any_section(self):
        """
        DESCRIPTION: Try to move slider or collapse/expand("-") any section
        EXPECTED: -   Popup message about logging out appears
        EXPECTED: -   User is logged out from the application and redirected to the Homepage
        EXPECTED: -   User is not able to see Cash Out bet lines and to perform Cash Out operations
        EXPECTED: -   'Please log in to see your Cash Out bets.' message and 'Log In' button are shown
        """
        pass
